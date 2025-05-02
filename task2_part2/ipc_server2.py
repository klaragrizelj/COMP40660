import socket
import pickle
import os
import hashlib
import binascii

SOCK = "/tmp/PW_socket"

# Removing any previous socket instances
if os.path.exists(SOCK):
    os.remove(SOCK)

# Creating the UNIX socket, then binding the path and then listening for the connection
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCK)
print("Server-PW: socket bound at", SOCK, flush=True)

server.listen(1)
print("Server-PW: waiting for connection...", flush=True)

# Accepting the connection from the client
conn, _ = server.accept()
print("Server-PW: connection established!", flush=True)

# Server receives the password sent by the client
password = pickle.loads(conn.recv(4096))
pw_bytes = password.encode("utf-8")

# Deriving a hash with PBKDF2-HMAC-SHA256 and random salt
salt = os.urandom(16)
iterations = 100_000
key = hashlib.pbkdf2_hmac("sha256", pw_bytes, salt, iterations)

# Converting the salt and the hash to hex
resp = {
    "salt":    binascii.hexlify(salt).decode(),
    "hash":    binascii.hexlify(key).decode(),
    "iterations": iterations
}

# Printing the result
print("Server-PW: generated hash:", resp, flush=True)

# Sending the result back to the client
conn.send(pickle.dumps(resp))
print("Server-PW: sent hash, exiting.", flush=True)

conn.close()
server.close()
os.remove(SOCK)
