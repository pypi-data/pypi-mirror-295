import sqlite3 as lite

class SqlSys:
    def __init__(self, db_name: str):
        self.conn = lite.connect(db_name)

    def add_User(self, username: str, password: str):
        cursor = self.conn.cursor()
        query = f"INSERT INTO users VALUES(?,?)"
        cursor.execute(query, (username, password))
        self.conn.commit()
        cursor.close()
    
    def login_user(self, username, password):
        cursor = self.conn.cursor()
        query = f"SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))

        if cursor.fetchone():
            cursor.close()
            return 0
        else:
            cursor.close()
            return 1

    def closeDB(self):
        self.conn.close()