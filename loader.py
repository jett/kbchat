import csv
from sentence_transformers import SentenceTransformer
import sqlite3
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
import openai


COMPLETIONS_MODEL = "gpt-3.5-turbo"
# make sure to set OPENAI_API_KEY

def construct_prompt(question: str):
    question_embedding = model.encode(question)
    search_params = {
        "metric_type": "l2",
        "params": {"nprobe": 10},
    }

    dbconn = sqlite3.connect("data.sqlite")
    cur = dbconn.cursor()

    collection = Collection(COLLECTION_NAME)
    collection.load()
    results = collection.search(data=[question_embedding], param=search_params, anns_field="embeddings", limit=2)

    SEPARATOR = "\n* "
    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""
    potential_answers = []

    for hits in results:
        for hit in hits:
            # print(f"hit: {hit}")
            cur.execute(f"SELECT content from kb where id = {hit.id}")
            content_data = cur.fetchone();
            # print(content_data[0])
            # potential_answers.append(SEPARATOR + str(hit.id))
            potential_answers.append(SEPARATOR + content_data[0])

    prompt = header + "".join(potential_answers) + "\n\n Q: " + question + "\n A:"
    print(prompt)

    message = [
        {"role": "system", "content": "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say \"I don't know.\""},
        {"role": "user", "content": prompt},
    ]

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    # print(gpt_response)
    return gpt_response["choices"][0]["message"]["content"].strip(" \n")


model = SentenceTransformer("sentence-transformers/gtr-t5-large")

connections.connect("default", host="localhost", port="19530")

COLLECTION_NAME = "qc_qa"
DIM_SIZE = 768
recreate_collection = True

dbconn = sqlite3.connect("data.sqlite")

if not utility.has_collection(COLLECTION_NAME) or recreate_collection:
    print("(re)creating collection")
    if utility.has_collection(COLLECTION_NAME) and recreate_collection:
        utility.drop_collection(COLLECTION_NAME)

    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=DIM_SIZE),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=500)
    ]

    schema = CollectionSchema(fields, "QC Q&A")
    qc_collection = Collection(COLLECTION_NAME, schema, consistency_level="Strong")

    ddl_command = """
    DROP TABLE IF EXISTS kb;
    CREATE TABLE kb (
        id INTEGER,
        content VARCHAR,
        PRIMARY KEY (id));
    """

    cur = dbconn.cursor()
    cur.executescript(ddl_command)

    ids = []
    embeddings = []
    texts = []

    with open("data/content.txt") as fd:
            rd = csv.reader(fd, delimiter="\t")
            next(rd, None)
            for row in rd:
                ids.append(row[0])
                embedding = model.encode(row[1])
                print(len(embedding))
                embeddings.append(embedding)
                texts.append(row[1])

                ins_rec = f"INSERT INTO kb (id, content) VALUES ('{row[0]}', '{row[1]}')"
                print(ins_rec)
                cur.execute(ins_rec)
                dbconn.commit()

    dbconn.close()

    entities = [
        [int(id) for id in ids],
        [embedding.tolist() for embedding in embeddings],
        [text for text in texts],
    ]

    insert_result = qc_collection.insert(entities)

    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }

    print("creating index")
    qc_collection.create_index("embeddings", index)
    print("done!")

# print("test search")
# response = construct_prompt("Who is responsible for approving policies?")
# print(response)
