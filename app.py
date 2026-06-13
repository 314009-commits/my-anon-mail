import sys
import io
import yagmail
import traceback
from flask import Flask, request
from flask_cors import CORS

# 強制終端機轉碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# ==================== 郵件伺服器設定 ====================
# ⚠️ 請在這裡輸入你的 Gmail 帳號與 16 位數密碼（中間有空格沒關係）
SENDER_EMAIL = "314009@sssh.tyc.edu.tw"
SENDER_PASSWORD = "khdviolcrfqmryrh"

RECEIVER_EMAIL = "314009@sssh.tyc.edu.tw"


# =======================================================

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        subject = request.form.get('subject', '').strip()
        message_content = request.form.get('message', '').strip()

        if not subject or not message_content:
            return "發送失敗：主題或內容不能為空", 400

        mail_body = f"收到一封新的匿名信件：\n\n{message_content}"

        print("🔄 正在嘗試透過 yagmail 安全發送郵件...")

        # 使用 yagmail 完美繞過 smtplib 的編碼錯誤
        yag = yagmail.SMTP(user=SENDER_EMAIL, password=SENDER_PASSWORD)
        yag.send(
            to=RECEIVER_EMAIL,
            subject=f"[匿名信] {subject}",
            contents=mail_body
        )

        print("🎉 郵件發送成功！")
        return "<h1>🎉 匿名信件已成功發送！</h1><p>對方將不會知道你是誰。</p>"

    except Exception as e:
        print("\n====== ⚠️ 偵測到後端錯誤 ======")
        traceback.print_exc()
        print("===============================\n")
        return f"<h1>❌ 郵件發送失敗</h1><p>錯誤訊息: {str(e)}</p>", 500


if __name__ == '__main__':
    import os
    # 優先讀取雲端分配的 Port，如果沒有（代表在自己電腦跑）就預設用 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)