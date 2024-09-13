import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def register():
	client.send("USERNAME_REGISTER".encode("utf-8"))
	
	username = input('Username :  ')
	client.send(username.encode("utf-8"))
	
	password = input('Password :  ')
	client.send(password.encode("utf-8"))

def login():
	client.send("USERNAME_LOGIN".encode("utf-8"))

	username = input('Username :  ')
	client.send(username.encode("utf-8"))
	
	password = input('Password :  ')
	client.send(password.encode("utf-8"))

def start_client_socket(host: str, port: int):
	adress = (host, port)
	client.connect(adress)	
	try:
		while True:
			choice = int(input('1. Login\n2. Register\n3. Exit\n\nchoice a number : '))
			if choice == 1:
				login()
			elif choice == 2:
				register()
			
			elif choice == 3:
				client.send('CLIENT_DISCONNECT'.encode("utf-8"))
				exit()
			else:
				print('Wrong number !')
	except KeyboardInterrupt:
		exit()

	finally:
		client.close()