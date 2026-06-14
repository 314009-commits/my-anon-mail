from flask import Flask, request
from flask_cors import CORS
import yagmail
import os

app = Flask(__name__)
CORS(app)

# 首頁測試用
@app.route("/")
def home():
    return "匿名信箱後端運作中"

# 真正寄信功能
@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        yag = yagmail.SMTP(
            user=os.environ["EMAIL_USER"],
            password=os.environ["EMAIL_PASSWORD"]
        )

        yag.send(
            to=os.environ["RECEIVER_EMAIL"],
            subject=f"[匿名信] {subject}",
            contents=message
        )

        return "success"

    except Exception as e:
        import traceback
        traceback.print_exc()   # 印完整錯誤到 Render Logs
        return str(e), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)