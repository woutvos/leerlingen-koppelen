from argon2 import PasswordHasher
import sqlite3


ph = PasswordHasher()


class admin:
    """This class is related to all things that have to do with the admin."""

    def check(username, password):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute('SELECT password FROM admin WHERE username = ?', (username,))
        rows = c.fetchall()
        
        password = ph.verify(rows[0][0], password)

        if password == True:
            return True
        return False
