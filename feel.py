import sys
import io
import yagmail
import traceback
from flask import Flask, request
from flask_cors import CORS

# 強制終端機轉碼避免中文字漏掉
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# ==================== 📬 郵件伺服器設定 ====================
# ⚠️ 請在這裡換上你的一般 Gmail 帳號與新的 16 位數應用程式密碼
SENDER_EMAIL = "leonchame374@gmail.com"
SENDER_PASSWORD = "mlpnbekkwhuxqidn"
RECEIVER_EMAIL = "leonchame374@gmail.com"
# =======================================================

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        subject = request.form.get('subject', '').strip()
        message_content = request.form.get('message', '').strip()

        if not subject or not message_content:
            return "發送失敗：主題或內容不能為空", 400

        mail_body = f"收到一封新的匿名信件：\n\n{message_content}"

        print("🔄 正在嘗試發送郵件...")

        # 🛠️ 我們把安全連線設定插在這裡！
        # 這樣個人 Gmail 走 465 SSL 安全通道才不會噴 500 錯誤
        yag = yagmail.SMTP(
            user=SENDER_EMAIL,
            password=SENDER_PASSWORD,
            host='smtp.gmail.com',
            port=465
        )
        yag.send(
            to=RECEIVER_EMAIL,
            subject=f"[匿名信] {subject}",
            contents=mail_body
        )

        print("🎉 郵件發送成功！")
        return "<h1>🎉 匿名信件已成功發送！</h1>"

    except Exception as e:
        print("\n====== ⚠️ 偵測到後端錯誤 ======")
        traceback.print_exc()
        print("===============================\n")
        return f"<h1>❌ 郵件發送失敗</h1><p>錯誤訊息: {str(e)}</p>", 500

if __name__ == '__main__':
    # 固定在本機的 5000 port 運行
    app.run(debug=True, port=5000)