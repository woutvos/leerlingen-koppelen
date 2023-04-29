import logging
import sqlite3

from utils.data import leerlingen
from utils.mail import mail_leerling


def remind():
    for student in leerlingen.get_list_reminder():
        mail_leerling.reminder(student)
        logging.info(f"Herinnering gestuurd naar {student}")


def create_database():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute(f"""
    CREATE TABLE "leerlingen" (
        "leerlingnummer"	NUMERIC,
        "naam"	INTEGER,
        "code"	TEXT,
        "voorkeur_1"	TEXT,
        "voorkeur_2"	TEXT,
        "voorkeur_3"	TEXT,
        "huidige_mentor"	TEXT,
        "nieuwe_mentor"	TEXT,
        PRIMARY KEY("leerlingnummer")
    )
    """)

    c.execute(f"""
    CREATE TABLE "mentoren" (
        "id"	NUMERIC,
        "naam"	TEXT,
        "code"	TEXT,
        "capaciteit"	INTEGER,
        "voorkeur_1"	TEXT,
        "voorkeur_2"	TEXT,
        "voorkeur_3"	TEXT,
        "voorkeur_4"	TEXT,
        "voorkeur_5"	TEXT,
        PRIMARY KEY("id")
    )
    """)

    c.execute(f"""
    CREATE TABLE "admin" (
        "username"	NUMERIC,
        "name"	TEXT NOT NULL,
        "password"	TEXT)
    """)

    conn.close()
