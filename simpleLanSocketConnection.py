import socket

def runServer():
    port = 8000  # Make sure it's within the > 1024 $$ <65535 range
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(1)

    physical_ip=(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[0] if ip.startswith("192.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    print("listening on "+str(physical_ip)+":"+str(port))
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print('From online user: ' + data)
        client_socket.send(data.encode('utf-8'))
    client_socket.close()

def runClient():
    import socket
    host = "192.168.0.148"  # "127.0.1.1"
    port = 8000  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.connect((host, port))

    message = input('Message: ')
    while message != 'q':
        s.send(message.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        print('Received from server: ' + data)
        message = input('Message: ')
    s.close()

while(True):
    print("welcome to Lan Chat")
    print("Run Server = 1")
    print("Run Client = 2")
    serverOrClient= input("Client or Server? :")
    if serverOrClient==1:
        runServer()
    if serverOrClient==2:
        runClient()
    else:
        print("not an option")


