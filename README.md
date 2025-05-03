# COMP40660
Assignment 2 - Edge Computing (Task 2)

Task 1: Basic Docker Virtualisation

1. Dockerised Environment Setup
- A dockerised environment was configured on a Linux-based VM.
- Docker was installed and verified using docker --version.

2. Three well-known Docker images were pulled and executed:
- hello-world: Verified successful Docker installation.
- busybox: Launched and used to run basic Linux commands.
- nginx: Deployed to serve a simple web server.

Viewing and cleaning Docker containers and images:
- Running containers were listing using
	docker ps -a
- All running containers were stopped and removed:
	docker stop $(docker ps -aq)
	docker rm $(docker ps -aq)
- Docker images were listed and removed:
	docker images
	docker rmi $(docker images -q)

3. Nginx custom web server with HTML page
- Followed the official Nginx Docker image guide:
https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/
- A custom HTML file with the group members names was created and mounted into the Nginx container.
- The file was served successfully at:
http://localhost:8080

4. Ubuntu container with package installation:
- A basic Ubuntu container was started:
	docker run -it ubuntu
- Installed packages such as nano and iputils-ping:
	apt update && apt install nano iputils-ping

5. Directory and file creation inside container:
- Created a directory named after the group:
	mkdir /GroupX
- Created a file members.txt and added the names:
	echo -e "Member 1\nMember 2\nMember 3" > /GroupX/members.txt  
	cat /GroupX/members.txt

	
6. Commit and push to Docker Hub:
The modified Ubuntu container was committed:
	docker commit <container_id> groupx/ubuntu-custom
- Image was tagged and pushed to Docker Hub:
	docker tag groupx/ubuntu-custom your_dockerhub_username/ubuntu-custom:v1  
	docker push your_dockerhub_username/ubuntu-custom:v1

Docker Hub Link: https://hub.docker.com/repositories/eannak


Task 2: Docker Networking 

1. Creating a custom docker network
   - Created a user-defined bridge network
     docker network create task2_network

2. Launching the three alpine containers
   - Launched the three containers
     docker run -dit --name alpine_cont1 --network task2_network alpine ash
     docker run -dit --name alpine_cont2 --network task2_network alpine ash
     docker run -dit --name alpine_cont3 --network task2_network alpine ash
     
3. Test of the container connections with ping commands
  - Ran the ping command three times to check connection on between each container
    docker exec -it alpine_cont1 ping -c 4 alpine_cont2
    docker exec -it alpine_cont2 ping -c 4 alpine_cont3
    docker exec -it alpine_cont3 ping -c 4 alpine_cont1
   
4. Establishing an Inter-Process Communication (IPC) channel between two Ubuntu containers
   - Created a directory to store all files
     mkdir task2_part1
   - First python file ipc_server.py was created
   - ipc_server.py listens to the UNIX socket, establishes a connection and receives data from the client
   - After receiving the data, ipc_server.py computes the mean, median and standard deviation of these values and displays results
   - Second python file ipc_client.py is was created, this represents the offloading client
   - ipc_client.py connects to the server and sends a list of 100 integer values
   - ipc_client.py receives the results from the server and displays it
   - Dockerfile is created, this file sets up the environment to run the IPC scripts, it is based on the latest Ubuntu image
   - docker-compose.yml file was created to automate and simplify the setup of the containers
   - docker-compose.yml file first builds the image, then runs the ipc_server.py, then runs the ipc_client.py
   - The program is tested using the following command:
     docker-compose up --build
   
5. The password hashing offloading scenario for future applications:
   - This scenario uses the same approach as before
   - ipc_client.py and ipc_server.py files are changed to accomodate the desired function (password hashing)
   - A new directory was created
     mkdir task2_part2
   - ipc_server.py was created
   - ipc_server.py creates the UNIX socket, listens to a connection, accepts the connection from the client,
     receives the password sent by a client, derives a hash with PBKDF2-HMAC-SHA256 algorithm, which is in a built-in
     Pyhon function, and random salt, converts the salt and hash to hex and send the results to the client
   - ipc_client.py was created
   - ipc_client.py prompts the user to put in a password in plaintext, sends it to the server and then receives the hashed password
   - The program is tested using the following sequence of commands:
     docker-compose build hash-server
     docker-compose build hash-client
     docker-compose up -d hash-server; docker-compose run --rm hash-client; docker-compose down

     GitHub link with Task2 2: https://github.com/klaragrizelj/COMP40660








   

