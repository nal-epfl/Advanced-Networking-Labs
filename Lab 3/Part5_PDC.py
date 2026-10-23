import socket
import ssl
import sys
from time import sleep

HOST = '127.0.0.1'
PORT = 5003
BUFFER_SIZE = 1024

if len(sys.argv) != 3:
    print('usage: %s <command> <path to CA certificate>' % sys.argv[0])
    sys.exit(1)

d = sys.argv[1]
filecert = sys.argv[2]

# Python 3.10 TLS Configuration
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(filecert)
ctx.check_hostname = False

ssl_s1 = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    s1 = socket.socket(af, socktype, proto)
    ssl_s1 = ctx.wrap_socket(s1, server_hostname=HOST)
    ssl_s1.connect(sa)
    print('ssl_s1: ', ssl_s1)
    break

message = d
ssl_s1.send(message.encode('utf-8'))
print("sending:", message)

RETRIES_1 = 100
for i in range(0, RETRIES_1):
    try:
        data = ssl_s1.recv(BUFFER_SIZE).decode('utf-8')
        if not data:
            break
        print('User 1 received:', data, '\n')
    except Exception as e:
        print("Connection closed or error:", e)
        break
    sleep(1)

while True:
    pass