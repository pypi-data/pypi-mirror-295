import socket
import threading

def bind_server(host:str, port:int):
    global server 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

def chat(nickname: str):
    global client, addr
    client, addr = server.accept()

    while True:
        msg = client.recv(1024).decode("utf-8")

        if msg == "quit":
            client.send(f"[INFO] {nickname} its leave the channel".encode("utf-8"))
            break
        else:
            print(msg)
        
        
        client.send(input('Msg: ').encode("utf-8"))
    client.close()