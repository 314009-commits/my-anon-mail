from flask import Flask, request
from flask_cors import CORS
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "匿名信箱後端運作中"

@app.route("/send_email", methods=["POST"])
def send_email():

    try:

        msg = MIMEText("Hello")
        msg["Subject"] = "測試信"
        msg["From"] = os.environ["EMAIL_USER"]
        msg["To"] = os.environ["RECEIVER_EMAIL"]

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=20
        )

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)