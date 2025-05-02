FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ipc_server2.py ipc_client2.py ./

CMD ["bash"]
