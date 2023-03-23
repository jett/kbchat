import csv
from sentence_transformers import SentenceTransformer
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

COLLECTION_NAME = "qc_qa"
DIM_SIZE = 768


model = SentenceTransformer("sentence-transformers/gtr-t5-large")

connections.connect("default", host="localhost", port="19530")

print(utility.has_collection(COLLECTION_NAME))
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False, max_length=100),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=DIM_SIZE)
]

schema = CollectionSchema(fields, "QC Q&A")
hello_milvus = Collection(COLLECTION_NAME, schema, consistency_level="Strong")

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

print(ids)

entities = [
    [int(id) for id in ids],
    [embedding.tolist() for embedding in embeddings]
]

insert_result = hello_milvus.insert(entities)
