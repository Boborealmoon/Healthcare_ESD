from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

appointments_url = environ.get('appointments_url') or "http://localhost:5000/appointments"
calendar_url = environ.get('calendar_url') or "http://localhost:5001/calendar"
claims_url = environ.get('claims_url') or "http://localhost:5002/new_claim"
employees_url = environ.get('employees_url') or "http://localhost:5003/employees"
inventory_url = environ.get('inventory_url') or "http://localhost:5004/inventory"
order_url = environ.get('order_url') or "http://localhost:5005/order"
patients_url = environ.get('patients_url') or "http://localhost:5006/patient"
email_service_url = environ.get('email_service') or "http://localhost:5010/email_service"

exchangename = "clinic_topic" # exchange name
exchangetype="topic" # use a 'topic' exchange to enable interaction

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

@app.route("/submit_claims", methods=['POST'])
def submit_claims():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            print(request.get_json())
            claim = request.get_json()
            print("\nSubmitted a claim in JSON:", claim)
            
            # Send claim info {claim items}
            result = processSubmitClaim(claim)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "submit_claims.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processSubmitClaim(claim):
    # Send the claim info {claim items}
    # Invoke the claims.py microservice
    print('\n-----Invoking claims microservice-----')
    claim_result = invoke_http(claims_url, method='POST', json=claim)
    print('claim_result:', claim_result)
    
    # Check the claim submission result; if a failure, send it to the error microservice.
    code = claim_result["code"]

    patient_id = claim_result["data"]["PatientID"]
    # Ensure that 'data' key exists in claim_result before accessing 'PatientID'

    print('\n-----Invoking patients microservice-----')
    patient_result = invoke_http(patients_url + f"/ID/{patient_id}", method='GET')
    print('patient_result:', patient_result)

    message = json.dumps(claim_result)
 
    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (claim error) message with routing_key=claim.error-----')

        # invoke_http(error_URL, method="POST", json=claim_result)
        channel.basic_publish(exchange=exchangename, routing_key="claim.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nClaim submission status ({:d}) published to the RabbitMQ Exchange:".format(
            code), claim_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"claim_result": claim_result},
            "message": "Claim submission failure sent for error handling."
        }

    # Publish to "Activity Log" only when there is no error in claim submission.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    else:
        patient_email = patient_result['data']['Email']
        patient_appointmentid = claim_result['data']['AppointmentID']

        print('\n\n-----Invoking appointments microservice-----')
        update_data = {
            "AppointmentID": patient_appointmentid,  # Replace with the actual appointment ID
            "Claimed": True  # Replace with the updated claim status
        }

        # Invoke the appointments microservice to update the appointment
        update_result = invoke_http(appointments_url + f'/{patient_id}/{patient_appointmentid}', method='PUT', json=update_data)
        print(update_result)

        # Send an email function
        email_data = {
            "recipient_email": patient_email,
            "subject": "Claim Submission Confirmation",
            "message_body": f"Dear patient,\n\nYou have successfully submitted a claim for your appointment.\n\nThank you!"
        }

        print('\n\n-----Invoking email microservice-----')
        email_result = invoke_http(email_service_url, method='POST', json=email_data)
        print(email_result)
        # Record new claim, record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (claim info) message with routing_key=claim.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=claim_result)            
        channel.basic_publish(exchange=exchangename, routing_key="claim.info", body=message)
    
        print("\nClaim submission published to RabbitMQ Exchange.\n")
        # - reply from the invocation is not used;
        # continue even if this invocation fails

        # 7. Return created claim
        return {
            "code": 201,
            "data": {
                "claim_result": claim_result,
            }
        }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
        " for creating a claim...")
    app.run(host="0.0.0.0", port=5300, debug=True)
