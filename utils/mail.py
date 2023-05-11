import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

from utils.data import leerlingen


class mail_leerling:
    """This class contains all the functions for sending emails to students."""

    def voorkeur(leerlingnummer, code):
        load_dotenv()

        host = os.getenv("HOST")
        port = os.getenv("PORT")
        naam = leerlingen.get_naam(leerlingnummer)

        html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Je persoonlijke code</title>
</head>

<body style='margin: 0; padding: 0; font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; overflow: hidden;'>
    <div style='padding: 80px; text-align: center; background: #1e91d6; color: white;'>
        <h1>Geef je voorkeur op!</h1>
        <p>Het is tijd om je voorkeur voor mentoren op te geven, in deze mail leggen we uit hoe je dit kunt doen!</p>
    </div>

    <div style='padding: 1px 16px; width: 600px; margin: 0 auto; padding-bottom: 100px; display: inline;'>
        <br>
        <p>Beste {naam},</p>
        <p>Hierbij ontvang je een mail met de uitleg van het invullen voor je voorkeuren.</p>
        <p>Volg de hieronder weergegeven stappen om het tot een succes te leiden!</p>
        <ol>
            <li>Open de website <a href="https://voorkeur.corderius.nl">voorkeur.corderius.nl</a></li>
            <li>Vul je leerlingnummer en persoonlijke code in</li>
            <li>Klik op de knop "Voorkeuren invullen"</li>
            <li>Zoek eerst de mentoren die je wel ziet zitten, klik vervolgens op "volgende"</li>
            <li>Bepaal nu de volgorde van de mentoren die je het liefst wilt, klik vervolgens op "volgende"</li>
            <li>Controleer of het klopt en bevestig je voorkeuren</li>
        </ol>
        <p class="code">Jouw persoonlijke code is: {code}</p>
        <a class="button" style='
            border: none;
            border-radius: 10px;
            box-shadow: 2px 2px 2px rgba(0,0,0,0.2);
            color: white;
            display: inline-block;
            font-size: 1em;
            padding: 1em 2em;
            width: auto;
            background-color: #5cdb5c;
            text-align: center;
            text-decoration: none;'
            margin-bottom: 1em;
        href="https://voorkeur.corderius.nl">Geef je voorkeur op!
        </a>
        <p>Met vriendelijke groet,</p>
        <p>Corderius College</p>
        <hr>
    </div>

    <div style='padding: 1px; text-align: center; background: #ddd; color: black; text-align: center; text-decoration: none;'>
        <!-- Contact informatie -->
        <p>Heb je vragen? Neem dan contact met ons op!</p>
        <p>E-mail: <a href="mailto:mail@woutvos.nl">mail@woutvos.nl</a></p>
    </div>
</body>
</html>
        """

        email_message = MIMEMultipart()
        email_message["From"] = os.getenv("EMAIL")
        email_message["Subject"] = "Geef je voorkeur op!"
        email_message["To"] = f"{leerlingnummer}@corderius.nl"

        email_message.attach(MIMEText(html, "html"))
        email_string = email_message.as_string()

        server = smtplib.SMTP(f"{host}: {port}")
        server.starttls()
        server.login(os.getenv("EMAIL"), os.getenv("EMAIL_WACHTWOORD"))
        server.sendmail(email_message["From"],
                        email_message["To"], email_string)
        server.quit()

        print(
            f"Mail verzonden naar {leerlingnummer}@corderius.nl met code: {code}")

    def uitslag(leerlingnummer, mentor, klas):
        load_dotenv()

        host = os.getenv("HOST")
        port = os.getenv("PORT")
        naam = leerlingen.get_naam(leerlingnummer)

        html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Je mentor is bekend!</title>
</head>

<body style='margin: 0; padding: 0; font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; overflow: hidden;'>
    <div style='padding: 80px; text-align: center; background: #1e91d6; color: white;'>
        <h1>Je mentor is bekend!</h1>
    </div>

    <div style='padding: 1px 16px; width: 600px; margin: 0 auto; padding-bottom: 100px; display: inline;'>
        <br>
        <p>Beste {naam},</p>
        <p>Je bent geplaatst in {klas}, bij meneer/mevrouw {mentor}. We hopen dat jij blij bent met je mentor!</p>
        <p>Dit is het eerste jaar dat leerlingen op deze manier worden gekoppeld aan mentoren. Na uitvoerig testen hopen we dat alles gewerkt heeft en het invullen makkelijk was. Wij horen graag feedback op deze website en alles eromheen.</p>
        <a class="button" style='
            border: none;
            border-radius: 10px;
            box-shadow: 2px 2px 2px rgba(0,0,0,0.2);
            color: white;
            display: inline-block;
            font-size: 1em;
            padding: 1em 2em;
            width: auto;
            background-color: #5cdb5c;
            text-align: center;
            text-decoration: none;'
            margin-bottom: 1em;
        href="https://feedback.corderius.nl">Geef feedback!
        </a>
        <p>Met vriendelijke groet,</p>
        <p>Corderius College</p>
        <hr>
    </div>

    <div style='padding: 1px; text-align: center; background: #ddd; color: black; text-align: center; text-decoration: none;'>
        <!-- Contact informatie -->
        <p>Heb je vragen? Neem dan contact met ons op!</p>
        <p>E-mail: <a href="mailto:mail@woutvos.nl">mail@woutvos.nl</a></p>
    </div>
</body>
</html>
        """

        email_message = MIMEMultipart()
        email_message["From"] = os.getenv("EMAIL")
        email_message["Subject"] = "Je mentor is bekend!"
        email_message["To"] = f"{leerlingnummer}@corderius.nl"

        email_message.attach(MIMEText(html, "html"))
        email_string = email_message.as_string()

        server = smtplib.SMTP(f"{host}: {port}")
        server.starttls()
        server.login(os.getenv("EMAIL"), os.getenv("EMAIL_WACHTWOORD"))
        server.sendmail(email_message["From"],
                        email_message["To"], email_string)
        server.quit()

        print(f"Uitslag verzonden naar {leerlingnummer}@corderius.nl")

    def reminder(leerlingnummer):
        load_dotenv()

        host = os.getenv("HOST")
        port = os.getenv("PORT")
        naam = leerlingen.get_naam(leerlingnummer)

        html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder: vul je voorkeur in</title>
</head>

<body style='margin: 0; padding: 0; font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; overflow: hidden;'>
    <div style='padding: 80px; text-align: center; background: #1e91d6; color: white;'>
        <h1>Reminder: vul je voorkeur in</h1>
    </div>

    <div style='padding: 1px 16px; width: 600px; margin: 0 auto; padding-bottom: 100px; display: inline;'>
        <br>
        <p>Beste {naam},</p>
        <p>Helaas is uit ons systeem gebleken dat jij je voorkeur nog niet hebt ingevuld.</p>
        <p>Je hebt nog tot eind deze week om dit te doen! Doe je dit niet, dan wordt er een random keuze ingevuld.</p>
        <p>Lukt het niet om je voorkeur in te vullen? Neem dan contact op via: <a href="mailto:mail@woutvos.nl">mail@woutvos.nl</a>.</p>
        <a class="button" style='
            border: none;
            border-radius: 10px;
            box-shadow: 2px 2px 2px rgba(0,0,0,0.2);
            color: white;
            display: inline-block;
            font-size: 1em;
            padding: 1em 2em;
            width: auto;
            background-color: #5cdb5c;
            text-align: center;
            text-decoration: none;'
            margin-bottom: 1em;
        href="https://voorkeur.corderius.nl">Geef je voorkeur op!
        </a>
        <p>Met vriendelijke groet,</p>
        <p>Corderius College</p>
        <hr>
    </div>

    <div style='padding: 1px; text-align: center; background: #ddd; color: black; text-align: center; text-decoration: none;'>
        <!-- Contact informatie -->
        <p>Heb je vragen? Neem dan contact met ons op!</p>
        <p>E-mail: <a href="mailto:mail@woutvos.nl">mail@woutvos.nl</a></p>
    </div>
</body>
</html>
"""

        email_message = MIMEMultipart()
        email_message["From"] = os.getenv("EMAIL")
        email_message["Subject"] = "Reminder: vul je voorkeur in"
        email_message["To"] = f"{leerlingnummer}@corderius.nl"

        email_message.attach(MIMEText(html, "html"))
        email_string = email_message.as_string()

        server = smtplib.SMTP(f"{host}: {port}")
        server.starttls()
        server.login(os.getenv("EMAIL"), os.getenv("EMAIL_WACHTWOORD"))
        server.sendmail(email_message["From"],
                        email_message["To"], email_string)
        server.quit()

        print(f"Reminder send to {leerlingnummer}@corderius.nl")
