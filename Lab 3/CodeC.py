import socket

HOST = "localhost"
PORT = 5008

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

message = "To connect, or not to connect, that is the TCP question. "
print("sending:", message)
sock.sendall(message.encode())
	
received = 0
expected = len(message)
	
while received < expected:
	data = sock.recv(20).decode()
	received += len(data)
	print ('received:', data)

while True:
	pass
