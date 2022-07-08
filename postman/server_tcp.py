import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='localhost'
PORT=5120
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
    if command[0]=='rfid':
        print(f"UID {command[1]}")
        server.send("Received UID".encode('utf-8'))
    if command[0]=='key':
        print(f"keypad {command[1]}")
        server.send("Received key".encode('utf-8'))
    if command[0]=='imageI': #incoming image binary stream
        print('creating image')
        f = open('pic.png',"wb")
        while True:
            image = server.recv(1024)
            if str(image) == "b''":
                break
            f.write(image)
        server.send("Image Received succesfuly".encode('utf-8'))