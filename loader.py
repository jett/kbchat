import csv
from sentence_transformers import SentenceTransformer
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)


model = SentenceTransformer("sentence-transformers/gtr-t5-large")

connections.connect("default", host="localhost", port="19530")

COLLECTION_NAME = "qc_qa"
DIM_SIZE = 768
recreate_collection = False

if not utility.has_collection(COLLECTION_NAME) or recreate_collection:
    print("(re)creating collection")
    utility.drop_collection(COLLECTION_NAME)

    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False, max_length=100),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=DIM_SIZE)
    ]

    schema = CollectionSchema(fields, "QC Q&A")
    qc_collection = Collection(COLLECTION_NAME, schema, consistency_level="Strong")

    ids = []
    embeddings = []

    with open("data/content.txt") as fd:
            rd = csv.reader(fd, delimiter="\t")
            next(rd, None)
            for row in rd:
                ids.append(row[0])
                embedding = model.encode(row[1])
                print(len(embedding))
                embeddings.append(embedding)

    entities = [
        [int(id) for id in ids],
        [embedding.tolist() for embedding in embeddings]
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

print("test search")

question = "Who is responsible for approving policies?"
question_embedding = model.encode(question)
search_params = {
    "metric_type": "l2",
    "params": {"nprobe": 10},
}

collection = Collection(COLLECTION_NAME)
collection.load()
results = collection.search(data=[question_embedding], param=search_params, anns_field="embeddings", limit=2)

for hits in results:
    for hit in hits:
        print(f"hit: {hit}")
