import socket

@app.route("/send_email", methods=["POST"])
def send_email():

    try:
        socket.create_connection(("smtp.gmail.com", 587), timeout=10)

        return "SMTP OK"

    except Exception as e:
        return str(e), 500