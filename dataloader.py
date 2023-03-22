import csv
from towhee import pipe, ops
import numpy as np
from towhee.datacollection import DataCollection

insert_pipe = (
    pipe.input('id', 'content')
        .map('content', 'vec', ops.text_embedding.dpr(model_name='facebook/dpr-ctx_encoder-single-nq-base'))
        .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
        .map(('id', 'vec'), 'insert_status', ops.ann_insert.milvus_client(host='127.0.0.1', port='19530', collection_name='qc_answer'))
        .output()
)

def load_data():
    with open("data/content.txt") as fd:
        rd = csv.reader(fd, delimiter="\t")
        for row in rd:
            print(row)

load_data()
