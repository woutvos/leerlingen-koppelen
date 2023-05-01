import hashlib
import logging
import random
import sqlite3
import string

from utils.mail import mail_leerling


class code:

    def gen_all():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM leerlingen")
        rows = c.fetchall()

        logging.info(
            "Gestart met het genereren van codes voor alle leerlingen"
        )

        for row in rows:
            leerlingnummer = row[0]

            code = "".join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(6))
            mail_leerling.voorkeur(leerlingnummer, code)
            code = hashlib.sha256(code.encode("utf-8")).hexdigest()

            c.execute(
                f'UPDATE leerlingen SET code = "{code}" WHERE leerlingnummer = {leerlingnummer}'
            )
            conn.commit()

        conn.close()

        logging.info(
            "Alle codes zijn gegenereerd en verstuurd naar de leerlingen")

    def gen_single(leerlingnummer):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        code = "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(6))
        mail_leerling.voorkeur(leerlingnummer, code)
        code = hashlib.sha256(code.encode("utf-8")).hexdigest()

        c.execute(
            f'UPDATE leerlingenSET code = "{code}" WHERE leerlingnummer = {leerlingnummer}'
        )
        conn.commit()

        conn.close()

        logging.info(
            f"Code is hergegenereerd en verstuurd naar leerling {leerlingnummer}"
        )

    def check_leerling(leerling, code):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        code = hashlib.sha256(code.encode("utf-8")).hexdigest()

        c.execute(
            f'SELECT * FROM leerlingen WHERE leerlingnummer = {leerling} AND code = "{code}"'
        )
        rows = c.fetchall()

        if len(rows) == 0:
            return False
        return True

    def check_mentor(mentor, code):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        code = hashlib.sha256(code.encode("utf-8")).hexdigest()

        c.execute(
            f'SELECT * FROM mentoren WHERE id = {mentor} AND code = "{code}"'
        )
        rows = c.fetchall()

        if len(rows) == 0:
            return False
        return True
