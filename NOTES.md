milvus
https://github.com/milvus-io/embd-milvus

please do the following if you haven not already done so:
1. install required dependencies: bash /var/bin/e-milvus/lib/install_deps.sh
2. export LD_PRELOAD=/home/jett/projects/kbchat/.venv/lib/python3.9/site-packages/milvus/bin/embd-milvus.so
3. (on Linux systems) export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib:/usr/local/lib:/var/bin/e-milvus/lib/
   (on MacOS systems) export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/lib:/usr/local/lib:/var/bin/e-milvus/lib/


# need tbb2
sudo apt-get install libtbb2