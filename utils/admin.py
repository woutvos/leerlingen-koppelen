import hashlib
import sqlite3


class admin:
    """This class is related to all things that have to do with the admin."""

    def check(username, password):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
        
        rows = c.fetchall()

        if len(rows) == 0:
            return False
        return True
