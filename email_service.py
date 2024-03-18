# email_service.py

from flask import Flask
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
mail = Mail(app)


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Update with your SMTP server
app.config['MAIL_PORT'] = 465  # Update with your SMTP port
app.config['MAIL_USERNAME'] = 'kevanteoty@gmail.com'  # Update with your email credentials
app.config['MAIL_PASSWORD'] = 'fqtm blbt asgh yzce'  # Update with your email credentials
app.config['MAIL_DEFAULT_SENDER'] = 'kevanteoty@gmail.com'  # Update with your email address
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/email_service", methods=['POST'])
def send_email():
    data = request.get_json()
    recipient_email = data.get('recipient_email')
    subject = data.get('subject')
    message_body = data.get('message_body')

    msg = Message(subject, recipients=[recipient_email])
    msg.body = message_body

    try:
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"message": "Error sending email", "error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
