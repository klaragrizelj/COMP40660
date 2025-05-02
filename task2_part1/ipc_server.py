import socket 
import pickle
import statistics
import os 

# Path to the UNIX domain socket 
SOCK = "/tmp/IPC_socket"

# Removal of any previous socket files to avoid erros 
if os.path.exists(SOCK):
	os.remove(SOCK)

# Creating a new UNIX socket and binding it to the defined path
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCK)

print("Server: Socket created at:", SOCK, flush=True)

# Server listens to the client connections
server.listen(1)

print("Server: Waiting for a connection ...", flush=True)

# Accepting only 1 connection from the client
conn, _ = server.accept()

print("Server: The connection is established!", flush=True)

# Server receives the data from the client and converts it from bytes to numbers
data = pickle.loads(conn.recv(4096))

# Server computes the mean, median and standard deviation from the received values
results = {
	'mean': statistics.mean(data),
    'median': statistics.median(data),
	'standard_deviation': statistics.stdev(data)
}

# Printing the results on the server side
print("Calculation results:", flush=True)
for k, v in results.items():
	print(f"{k:<20}: {v:.4f}", flush=True)

# Server converts the results in numbers back to bytes and sends it to the client
conn.send(pickle.dumps(results))

print("Server: Calculation results sent to the client!", flush=True)

# Closing the connection
conn.close()
server.close()
os.remove(SOCK)
