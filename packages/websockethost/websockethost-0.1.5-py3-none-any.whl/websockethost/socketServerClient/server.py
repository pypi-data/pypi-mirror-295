import socket
from ThreadScripts.ThreadForClient import ThreadForClient

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_socket_server(host: str, port: int, log_file: str):
	adress = ("localhost", 5500)
	server.bind(adress)	
	while True:
		try:
			server.listen(5)
			client, addr = server.accept()

				
			with open("conn.log", "a+") as logs:
				logs.write(f"The connection as create on : {addr}")

			my_thread = ThreadForClient(client)
			my_thread.start()
			
		except KeyboardInterrupt:
			break

	client.close()
	server.close()
