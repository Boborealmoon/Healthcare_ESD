# email_service.py

from flask import Flask
from flask_mail import Mail, Message
from flask import Flask, request, jsonify

app = Flask(__name__)
mail = Mail(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Update with your SMTP server
app.config['MAIL_PORT'] = 465  # Update with your SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'teokevan@gmail.com'  # Update with your email credentials
app.config['MAIL_PASSWORD'] = ''  # Update with your email credentials
app.config['MAIL_DEFAULT_SENDER'] = 'teokevan@gmail.com'  # Update with your email address

@app.route("/send_email", methods=['POST'])
def send_email():
    data = request.get_json()
    recipient_email = data.get('recipient_email')
    subject = data.get('subject')
    message_body = data.get('message_body')

    msg = Message(subject, recipients=[recipient_email])
    msg.body = message_body
    mail.send(msg)

    return "Email sent successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009)
