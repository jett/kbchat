from pymilvus import Milvus, utility, connections
from sentence_transformers import SentenceTransformer
import csv

model = SentenceTransformer("sentence-transformers/gtr-t5-large")

host = '127.0.0.1'
port = '19530'
client = Milvus(host, port)

cols = client.list_collections()
print(cols)


def load_data():

    ids = []
    embeddings = []

    collection_name = 'qc_answer'

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
        # [int(id) for id in ids],
        [embedding.tolist() for embedding in embeddings]
    ]

    print(entities)
    # status, myids = client.insert(collection_name='qc_answer', entities=entities)

def query_data():
    pass

load_data()
