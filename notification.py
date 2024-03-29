from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
# import pika
import os

app = Flask(__name__)

# Define the Twilio account SID and auth token
account_sid = "AC4b7413285dab6846b235ceff328da0a1"
auth_token = "550aef6908f9fe30160d81fc1c935e76"

print("Notification.py is now running------------------")


# Define the client object with the Twilio account SID and auth token
client = Client(account_sid, auth_token)

# Define the route to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    print("Now calling send_message function------------------")
    data = request.get_json()
    print(data)
    try:
        # Get the recipient's phone number and message from the request
        data = request.get_json()
        # to_number = data['contact']
        to_number = "+65 8218 9083"
        message = data['message_body']

        # Use the client object to send a message to the given phone number
        message = client.messages.create(
            to=to_number, # patient number
            from_="+12054984472", # my nummber
            body = message
        )
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