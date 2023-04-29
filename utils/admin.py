import hashlib
import sqlite3

class admin:
    def check(username, password):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        c.execute(f'SELECT * FROM admin WHERE username = "{username}" AND password = "{password}"')
        rows = c.fetchall()

        if len(rows) == 0:
            return False
        return True
