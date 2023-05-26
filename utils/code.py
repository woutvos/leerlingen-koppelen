import logging
import random
import sqlite3
import string

from argon2 import PasswordHasher

from utils.mail import mail_leerling, mail_mentor

ph = PasswordHasher()


class code:
    """This class contains all things that have to do with the codes from checking to generating."""

    def gen_leerlingen():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM leerlingen")
        rows = c.fetchall()

        logging.info(
            "Gestart met het genereren van codes voor alle leerlingen")

        for row in rows:
            leerlingnummer = row[0]

            code = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
            )
            mail_leerling.voorkeur(leerlingnummer, code)
            code = ph.hash(code)

            c.execute(
                "UPDATE leerlingen SET code = ? WHERE leerlingnummer = ?",
                (code, leerlingnummer),
            )
            conn.commit()

        conn.close()

        logging.info("Alle codes zijn gegenereerd en verstuurd naar de leerlingen")

    def gen_leerling(leerlingnummer):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        code = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
        )
        mail_leerling.voorkeur(leerlingnummer, code)
        code = ph.hash(code)

        c.execute(
            "UPDATE leerlingen SET code = ? WHERE leerlingnummer = ?",
            (code, leerlingnummer),
        )
        conn.commit()

        conn.close()

        logging.info(
            f"Code is hergegenereerd en verstuurd naar leerling {leerlingnummer}"
        )

    def check_leerling(leerling, code):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(
            "SELECT code FROM leerlingen WHERE leerlingnummer = ?", (leerling,))
        rows = c.fetchall()

        code = ph.verify(rows[0][0], code)

        if code == True:
            return True
        return False

    def check_mentor(mentor, code):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT code FROM mentoren WHERE id = ?", (mentor,))
        rows = c.fetchall()

        code = ph.verify(rows[0][0], code)

        if code == True:
            return True
        return False

    def gen_mentoren():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM mentoren")
        rows = c.fetchall()

        logging.info(
            "Gestart met het genereren van codes voor alle mentoren")

        for row in rows:
            id = row[0]

            code = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
            )
            mail_mentor.voorkeur(id, code)
            code = ph.hash(code)

            c.execute(
                "UPDATE mentoren SET code = ? WHERE id = ?",
                (code, id),
            )
            conn.commit()

        conn.close()

        logging.info("Alle codes zijn gegenereerd en verstuurd naar de mentoren")

    def gen_mentor(id):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        code = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
        )
        mail_leerling.voorkeur(id, code)
        code = ph.hash(code)

        c.execute(
            "UPDATE mentoren SET code = ? WHERE id = ?",
            (code, id),
        )
        conn.commit()

        conn.close()

        logging.info(
            f"Code is hergegenereerd en verstuurd naar mentor {id}"
        )
