import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='localhost'
PORT=5080
server.bind((HOST,PORT))
server.listen(1)
server,addr=server.accept()
print("Got a connection from",addr[0],":",addr[1])
while True:
    print("Waiting for command")
    data=server.recv(1024)
    data=data.decode('utf-8')
    print (data)
    command = data.split(' ')
    if command[0]=='quit':
        break
    