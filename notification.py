from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
# import pika
import os

app = Flask(__name__)

# Define the Twilio account SID and auth token
account_sid = "AC1cae7b4c166346f2c11c398c60d4334a"
auth_token = "bc53e86d97c6d74babf7f4695b78d58f"

print("Notification.py is now running------------------")

# Define the client object with the Twilio account SID and auth token
client = Client(account_sid, auth_token)

# Define the route to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    print("Now calling send_message function------------------")
    # data = request.get_json()
    try:
        # Get the recipient's phone number and message from the request
        data = request.get_json()
        message = data['message_body']
        to_number = "+6593877703"
        # Use the client object to send a message to the given phone number
        message = client.messages.create(
            from_='+13252406467',
            body = message,
            to='+6593877703'
        )
        # print(message.sid)
        print("Message is now sent--------------------------------")
        # Return the message SID
        return jsonify({
            "code": 200,
            'message_sid': message.sid
            })
    
    except TwilioRestException as e:
        print(f"Error sending message to {to_number}: {str(e)}")
        return jsonify(
        {
            "code": 404,
            "message": "Message failed to send ."
        }
    ), 404

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " sending message to patient.")
    app.run(host="0.0.0.0", port=5012, debug=True)