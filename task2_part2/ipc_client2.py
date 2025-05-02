import socket
import pickle
import os
import time
import getpass

SOCK = "/tmp/PW_socket"
# Client is waiting until server has created the socket 
while not os.path.exists(SOCK):
        time.sleep(0.05)

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCK)

# Client puts in a password that gets stored into getpass
password = getpass.getpass("Enter password to hash: ")

# The password in plaintext is sent to the server to get hashed 
client.send(pickle.dumps(password))

# The client then receives the hashed password
resp = pickle.loads(client.recv(4096))

print("Client-PW: received hash info:")
print(f"    salt      : {resp['salt']}")
print(f"    hash      : {resp['hash']}")
print(f"    iterations: {resp['iterations']}")
print("Client-PW: exiting.", flush=True)

client.close()
