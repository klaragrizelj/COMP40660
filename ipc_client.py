import socket 
import pickle
import os
import time

# The socket file path which is the same as the server socket file path
SOCK = "/tmp/IPC_socket"

# The client waits until the server creates the socket file
while not os.path.exists(SOCK):
	time.sleep(0.05)

# Creating and connecting to the UNIX socket
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCK)

# Client send a list of integer values from 1 to 100
client.send(pickle.dumps(list(range(1,101))))

# Client receives the dictionary with calculation results from the server
results = pickle.loads(client.recv(4096))

# Allowing the server to print the results first, before client prints it
time.sleep(0.1)

# Printing the calculation results
print("Client: The calculation results received from the server:", flush=True)
for k, v in results.items():
	print(f"{k:<20}: {v:.4f}", flush=True)

print("Client: Exiting!", flush=True)

# Closing the connection 
client.close()
