import logging
import sqlite3


class leerlingen:
    """This class contains all things that have to do with the students."""

    def get_voorkeuren():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        leerling_voorkeuren = {}

        for row in c.execute("SELECT * FROM leerlingen"):
            naam = row[1]
            voorkeur_1 = row[3]
            voorkeur_2 = row[4]
            voorkeur_3 = row[5]
            leerling_voorkeuren[naam] = [voorkeur_1, voorkeur_2, voorkeur_3]

        conn.close()

        return leerling_voorkeuren

    def get_naam(leerlingnummer):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f"SELECT naam FROM leerlingen WHERE leerlingnummer = {leerlingnummer}"
        )
        naam = c.fetchone()[0]
        conn.close()
        return naam

    def set_mentor(naam, mentor):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f'UPDATE leerlingen SET nieuwe_mentor = "{mentor}" WHERE naam = "{naam}"'
        )
        conn.commit()
        conn.close()

    def get_mentor(naam):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f'SELECT huidige_mentor FROM leerlingen WHERE naam = "{naam}"')
        mentor = c.fetchone()[0]
        conn.close()
        return mentor

    def set_voorkeur(leerlingnummer, voorkeur_1, voorkeur_2, voorkeur_3):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f'UPDATE leerlingen SET voorkeur_1 = "{voorkeur_1}", voorkeur_2 = "{voorkeur_2}", voorkeur_3 = "{voorkeur_3}" WHERE leerlingnummer = {leerlingnummer}'
        )
        conn.commit()
        conn.close()
        logging.info(
            f"Voorkeuren van leerling {leerlingnummer} zijn aangepast")

    def get_list_reminder():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        empty_preferences = []
        for row in c.execute("SELECT * FROM leerlingen"):
            leerlingnummer = row[0]
            voorkeur_1 = row[3]
            voorkeur_2 = row[4]
            voorkeur_3 = row[5]

            if voorkeur_1 is None or voorkeur_2 is None or voorkeur_3 is None:
                empty_preferences.append(leerlingnummer)
        conn.close()
        return empty_preferences


class mentoren:
    """This class contains all things that have to do with the mentors."""

    def get_voorkeuren():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        leerling_voorkeuren = {}

        for row in c.execute("SELECT * FROM mentoren"):
            naam = row[1]
            voorkeur_1 = row[4]
            voorkeur_2 = row[5]
            voorkeur_3 = row[6]
            voorkeur_4 = row[7]
            voorkeur_5 = row[8]
            leerling_voorkeuren[naam] = [
                voorkeur_1,
                voorkeur_2,
                voorkeur_3,
                voorkeur_4,
                voorkeur_5,
            ]

        conn.close()

        return leerling_voorkeuren

    def get_name(mentor):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(f"SELECT naam FROM mentoren WHERE id = {mentor}")
        naam = c.fetchone()[0]
        conn.close()
        return naam

    def set_voorkeur(mentor, voorkeur_1, voorkeur_2, voorkeur_3, voorkeur_4,
                     voorkeur_5):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f'UPDATE mentoren SET voorkeur_1 = "{voorkeur_1}", voorkeur_2 = "{voorkeur_2}", voorkeur_3 = "{voorkeur_3}", voorkeur_4 = "{voorkeur_4}", voorkeur_5 = "{voorkeur_5}" WHERE id = {mentor}'
        )
        conn.commit()
        conn.close()
        logging.info(f"Voorkeuren van mentor {mentor} zijn aangepast")

    def get_list():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        mentoren = {}

        for row in c.execute("SELECT * FROM mentoren"):
            id = row[0]
            naam = row[1]
            capaciteit = row[3]
            voorkeur_1 = row[4]
            voorkeur_2 = row[5]
            voorkeur_3 = row[6]
            voorkeur_4 = row[7]
            voorkeur_5 = row[8]
            mentoren[id] = [
                naam,
                capaciteit,
                voorkeur_1,
                voorkeur_2,
                voorkeur_3,
                voorkeur_4,
                voorkeur_5,
            ]

        conn.close()
        # sort the list by id
        mentoren = dict(sorted(mentoren.items()))
        return mentoren

    def get_allowed_students(mentor):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            f"SELECT leerlingnummer, naam FROM leerlingen WHERE voorkeur_1 = '{mentor}' OR voorkeur_2 = '{mentor}' OR voorkeur_3 = '{mentor}'"
        )
        allowed_students = [(row[0], row[1]) for row in c.fetchall()]
        conn.close()
        return allowed_students
