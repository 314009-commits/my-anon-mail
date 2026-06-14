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
    return "API OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)