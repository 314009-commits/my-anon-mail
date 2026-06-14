from flask import Flask
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/")
def home():
    return "SMTP 測試版"

@app.route("/send_email", methods=["POST"])
def send_email():
    try:

        msg = MIMEText("Hello")
        msg["Subject"] = "測試信"
        msg["From"] = os.environ["EMAIL_USER"]
        msg["To"] = os.environ["RECEIVER_EMAIL"]

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.starttls()

        server.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_PASSWORD"]
        )

        server.send_message(msg)
        server.quit()

        return "SEND OK"

    except Exception as e:
        import traceback
        traceback.print_exc()
        return str(e), 500