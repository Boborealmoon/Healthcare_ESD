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

appointments_url = "http://kong:8000/api/v1/appointments"  
calendar_url = "http://kong:8000/api/v1/calendar"   
patients_url = "http://kong:8000/api/v1/patient"   
email_service_url = "http://kong:8000/api/v1/emailservice"
notification_url = "http://kong:8000/api/v1/notification"

exchangename = "clinic_topic" # exchange name
exchangetype="topic" # use a 'topic' exchange to enable interaction

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

@app.route("/book_appointment", methods=['POST'])
def book_appointment():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            appointment = request.get_json()
            print("\nReceived an appointment in JSON:", appointment)

            # do the actual work
            # 1. Send appointment info
            result = processAppointmentbooking(appointment)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "book_appointment.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processAppointmentbooking(appointment):
    # 2. Send the appointment info {appointment items}
    # Invoke the appointment microservice
    print('\n-----Invoking appointments microservice-----')
    appointment_result = invoke_http(appointments_url, method='POST', json=appointment)
    print('appointment_result:', appointment_result)

    message = json.dumps(appointment_result)

    code = appointment_result["code"]
    if code not in range(200, 300):

        print('\n\n-----Publishing the (claim error) message with routing_key=claim.error-----')
        channel.basic_publish(exchange=exchangename, routing_key="appointment.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\n Appointment Creation Failure ({:d}) published to the RabbitMQ Exchange:".format(
            code), appointment_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"appointment_result": appointment_result},
            "message": "Appointment creation failure sent for error handling."
        }
    else:
        patient_id = appointment.get("PatientID")

        print('\n-----Invoking patients microservice-----')
        patient_result = invoke_http(patients_url + f"/ID/{patient_id}", method='GET')
        print('patient_result:', patient_result)
        patient_email = patient_result["data"]["Email"]

        patient_timeslot = appointment_result["data"]["TimeslotID"]

        print('\n-----Invoking calendar microservice-----')
        calendar_result = invoke_http(calendar_url + f"/{patient_timeslot}", method='GET')
        print('calendar_result:', calendar_result)
        
        patient_number = patient_result["data"]["ContactNo"]
        patient_name = appointment_result["data"]["PatientName"]
        appt_date = appointment_result["data"]["AppointmentDate"]
        appt_time = calendar_result["data"]["TimeBegin"]
        
        email_data = {
            "recipient_email": patient_email,
            "subject": "Appointment Confirmation",
            "message_body": f"Dear {patient_name},\n\nYour appointment has been successfully booked for {appt_date} at {appt_time}.\n\nThank you!"
        }
        
        sms_data = {
            "contact": patient_number,
            "message_body": f"Dear {patient_name},\n\nYour appointment has been successfully booked for {appt_date} at {appt_time}.\n\nThank you!"
        }

        print('\n\n-----Invoking email microservice-----')
        email_result = invoke_http(email_service_url, method='POST', json=email_data)
        print(email_result)

        print('\n\n-----Invoking notification microservice-----')
        notification_result = invoke_http(notification_url, method='POST', json=sms_data)
        print(notification_result)
        
        print('\n\n-----Publishing the (Appointment Info) message with routing_key=Appointment.info-----')        
            # invoke_http(activity_log_URL, method="POST", json=claim_result)            
        channel.basic_publish(exchange=exchangename, routing_key="appointment.info", body=message)
        
        print("\nAppointment Creation published to RabbitMQ Exchange.\n")

        return {
            "code": 201,
            "data": {
                "appointment":appointment_result,
                "patient":patient_result
            }
        }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for booking an appointment...")
    app.run(host="0.0.0.0", port=5200, debug=True)
