from SqlSys import SqlSys
import threading

class ThreadForClient(threading.Thread):
	def __init__(self, client, db_name: str):
		threading.Thread.__init__(self)
		self.client = client
		self.db_name = db_name

	def run(self):
		db_host = SqlSys(self.db_name)
		dataMSG = self.client.recv(1024).decode("utf-8")
		if dataMSG == "USERNAME_REGISTER":
			clientUsername = self.client.recv(1024).decode("utf-8")
			clientPassword = self.client.recv(1024).decode("utf-8")
			db_host.add_User(clientUsername, clientPassword)

		if dataMSG == "USERNAME_LOGIN":
			ClientLoginUsername = self.client.recv(1024).decode("utf-8")
			ClientLoginPassword = self.client.recv(1024).decode("utf-8")
			loginUser = db_host.login_user(ClientLoginUsername, ClientLoginPassword)

			if loginUser == 1:
				self.client.send("nom utilisateur/mot de passe invalide".encode("utf-8"))
			if loginUser == 0:
				self.client.send("Vous êtes connecté ! ".encode("utf-8"))
