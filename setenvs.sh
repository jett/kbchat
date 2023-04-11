#!/bin/bash

export LD_PRELOAD=/home/jett/projects/kbchat/.venv/lib/python3.9/site-packages/milvus/bin/embd-milvus.so
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib:/usr/local/lib:/var/bin/e-milvus/lib/ 
