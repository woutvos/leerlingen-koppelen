import sqlite3
import hashlib

def check_leerling(leerling, code):
    print(
        'SELECT * FROM leerlingen WHERE leerlingnummer = %s AND code = %s;' % (leerling, code)
    )

check_leerling(1, 2)