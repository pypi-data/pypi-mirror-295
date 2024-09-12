import socket 
import threading
import time, os

def connect(host:str, port:int):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect((host, port))

def chat(nickname:str):
        while True:
                client.send(input('Msg: ').encode("utf-8"))
                msg = client.recv(1024).decode("utf-8")
                
                if msg == "quit":
                        i = 0

                        while i < 5:
                                os.system("cls")
                                print('disconnecting.')
                                time.sleep(1)
                                os.system("cls")
                                print('disconnecting..') 
                                time.sleep(1)
                                os.system("cls")
                                print('disconnecting...')
                                time.sleep(1)
                                os.system("cls")
                                i += 1                       
                        break
                else:
                    print(msg)
                
        
        client.close()
