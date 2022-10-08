# multiClientServerLanIpTcp.py
import socket
import threading




def runServer():
    def start_listenning_thread(client):
        client_thread = threading.Thread(
            target=listen_thread,
            args=(client,)  # the list of argument for the function
        )
        client_thread.start()


    def listen_thread(client):
        while True:
            message = client.recv(1024).decode()
            if message:
                print(f"Received message : {message}")
                broadcast(message)
            else:
                print(f"client has been disconnected : {client}")
                return


    def broadcast(message):
        for client in broadcast_list:
            try:
                client.send(message.encode())
            except:
                broadcast_list.remove(client)
                print(f"Client removed : {client}")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 8000
    ADDRESS = "0.0.0.0"
    broadcast_list = []
    my_socket.bind((ADDRESS, PORT))
    physical_ip=(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[1] if ip.startswith("192.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    print("listening on "+str(physical_ip)+":"+str(PORT))
    while True:
        my_socket.listen()
        client, client_address = my_socket.accept()
        broadcast_list.append(client)
        start_listenning_thread(client)




def runClient():
    import socket
    import threading

    nickname = input("Choose your nickname : ").strip()
    while not nickname:
        nickname = input("Your nickname should not be empty : ").strip()
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Enter Host Physical Ip: ")
    port = 8000
    print(f"Trying to connect to: {host}:{port}")
    my_socket.connect((host, port))

    def thread_sending():
        while True:
            message_to_send = input("Enter message: ")
            if message_to_send:
                message_with_nickname = nickname + " : " + message_to_send
                my_socket.send(message_with_nickname.encode())

    def thread_receiving():
        while True:
            message = my_socket.recv(1024).decode()
            print(message)

    thread_send = threading.Thread(target=thread_sending)
    thread_receive = threading.Thread(target=thread_receiving)
    thread_send.start()
    thread_receive.start()


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
