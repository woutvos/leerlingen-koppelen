import logging
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_mobility import Mobility

from utils.admin import admin
from utils.code import code
from utils.data import leerlingen, mentoren
from utils.other import remind

app = Flask(__name__, template_folder="templates")
Mobility(app)
app.secret_key = "wk92ua3yfih8ts44v"
huidige_fase = 3
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


# Routes
@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/error/")
def error():
    return render_template("error.html", title="Error")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gebruikersnaam = request.form.get("gebruikersnaam")
        password_code = request.form.get("code")

        if huidige_fase == 2:
            if code.check_leerling(gebruikersnaam, password_code) is True:
                session["gebruikersnaam"] = gebruikersnaam
                logging.info(f"Leerling {gebruikersnaam} heeft ingelogd")
                return redirect(url_for("voorkeur"))
            logging.info(f"Code verkeerd ingevoerd voor {gebruikersnaam}")

        elif huidige_fase == 3:
            if code.check_mentor(gebruikersnaam, password_code) is True:
                session["gebruikersnaam"] = gebruikersnaam
                logging.info(f"Mentor {gebruikersnaam} heeft ingelogd")
                return redirect(url_for("voorkeur"))
            logging.info(f"Code verkeerd ingevoerd voor {gebruikersnaam}")

    if "gebruikersnaam" not in session:
        return render_template("login.html",
                               title="Login",
                               huidige_fase=huidige_fase)

    if "gebruikersnaam" in session:
        return redirect(url_for("voorkeur"))


@app.route("/voorkeur/", methods=["GET", "POST"])
def voorkeur():
    if "gebruikersnaam" not in session:
        return redirect(url_for("login"))

    if "gebruikersnaam" in session and huidige_fase == 2:
        return render_template(
            "voorkeur-leerling.html",
            title="Voorkeur",
            personen_lijst=mentoren.get_list().items(),
        )

    if "gebruikersnaam" in session and huidige_fase == 3:
        mentor = mentoren.get_name(session["gebruikersnaam"])
        return render_template(
            "voorkeur-mentor.html",
            title="Voorkeur",
            personen_lijst=mentoren.get_allowed_students(mentor),
        )


@app.route("/api/voorkeur/<device>/", methods=["POST"])
def set_voorkeur_leerling(device):
    if "gebruikersnaam" in session and huidige_fase == 2 and device != "mobile":
        gebruikersnaam = session["gebruikersnaam"]
        data = request.get_json()
        voorkeur_1 = data[0]["value"].replace("<p>", "").replace("</p>", "")
        voorkeur_2 = data[1]["value"].replace("<p>", "").replace("</p>", "")
        voorkeur_3 = data[2]["value"].replace("<p>", "").replace("</p>", "")

        leerlingen.set_voorkeur(gebruikersnaam, voorkeur_1, voorkeur_2,
                                voorkeur_3)
        return jsonify({"status": "success"})

    if "gebruikersnaam" in session and huidige_fase == 3 and device != "mobile":
        gebruikersnaam = session["gebruikersnaam"]
        data = request.get_json()
        voorkeur_1 = data[0]["value"].replace("<p>", "").replace("</p>", "")
        voorkeur_2 = data[1]["value"].replace("<p>", "").replace("</p>", "")
        voorkeur_3 = data[2]["value"].replace("<p>", "").replace("</p>", "")
        voorkeur_4 = data[3]["value"].replace("<p>", "").replace("</p>", "")
        voorkeur_5 = data[4]["value"].replace("<p>", "").replace("</p>", "")

        mentoren.set_voorkeur(gebruikersnaam, voorkeur_1, voorkeur_2,
                              voorkeur_3, voorkeur_4, voorkeur_5)
        return jsonify({"status": "success"})


@app.route("/bedankt/", methods=["GET"])
def bedankt():
    return render_template("bedankt.html", title="Bedankt!")


@app.route("/admin-login/", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_username = request.form.get("username")
        password = request.form.get("password")

        if admin.check(admin_username, password) is True:
            session["admin_username"] = admin_username
            logging.info(f"Admin {admin_username} heeft ingelogd")
            return redirect(url_for("dashboard"))
        logging.info(
            f"Wachtwoord verkeerd ingevoerd voor gebruiker {admin_username}")

    return render_template("admin-login.html", title="Admin login")


@app.route("/dashboard/", methods=["GET"])
def dashboard():
    if "admin_username" not in session:
        return redirect(url_for("admin_login"))

    if "admin_username" in session:
        return render_template("dashboard.html",
                               title="Dashboard",
                               huidige_fase=huidige_fase)


@app.route("/verander-fase/", methods=["GET", "POST"])
def verander_fase():
    global huidige_fase
    if "admin_username" not in session:
        return redirect(url_for("admin_login"))

    if "admin_username" in session:
        if request.method == "POST":
            fase = request.form.get("fase")
            if fase == "1":
                huidige_fase = 1
                logging.info("Fase 1 is gestart")

            if fase == "2":
                huidige_fase = 2
                logging.info("Fase 2 is gestart")

            if fase == "3":
                huidige_fase = 3
                logging.info("Fase 3 is gestart")

            if fase == "4":
                huidige_fase = 4
                logging.info("Fase 4 is gestart")

            if fase == "5":
                huidige_fase = 5
                logging.info("Fase 5 is gestart")

        return render_template("verander-fase.html", huidige_fase=huidige_fase)


@app.route("/fase1/", methods=["GET", "POST"])
def fase1():
    if request.method == "POST" and request.form.get("confirm") == "JA2023":
        if "admin_username" in session:
            code.gen_all()

    if request.method == "POST" and request.form.get(
            "leerlingnummer") is not None:
        if "admin_username" in session:
            code.gen_single(request.form.get("leerlingnummer"))

    if "admin_username" not in session:
        return redirect(url_for("admin_login"))

    if "admin_username" in session:
        return render_template("fase1.html", title="Fase 1")


@app.route("/fase2/", methods=["GET", "POST"])
def fase2():
    if request.method == "POST":
        if "admin_username" in session:
            remind()

    if "admin_username" not in session:
        return redirect(url_for("admin_login"))

    if "admin_username" in session:
        return render_template("fase2.html", title="Fase 2")


app.run(port=80, threaded=True)
