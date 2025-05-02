# Using the official Ubuntu base image
FROM ubuntu:latest

# Updating the package list and installing Python3
RUN apt-get update && apt-get install -y python3

# Setting the working directory inside the container
WORKDIR /app

# Copying the server and client scripts into the container
COPY ipc_server.py ipc_client.py ./

# Launching into bash
CMD ["/bin/bash"]

