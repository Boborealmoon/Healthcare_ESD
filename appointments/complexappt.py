from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

appointments_url = "http://localhost:5000/appointments"
# calendar_url = "http://localhost:5001/Clinic_calendar"
# claims_url = "http://localhost:5002/claims"
# employees_url = "http://localhost:5003/employee"
# inventory_url = "http://localhost:5004/inventory"
# order_url = "http://localhost:5005/order"
# patients_url = "http://localhost:5006/patient"

@app.route("/book_appointment", methods=['POST'])
def book_appointment():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            appointment = request.get_json()
            print("\nReceived an order in JSON:", appointment)

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
                "message": "complexappt.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processAppointmentbooking(appointment):
    # 2. Send the appointment info {appointment items}
    # Invoke the appointment microservice
    print('\n-----Invoking order microservice-----')
    appointment_result = invoke_http(appointments_url, method='POST', json=appointment)
    print('appointment_result:', appointment_result)

    return {
        "code": 201,
        "data": {
            "appointment":appointment_result
        }
    }
    # # 4. Record new order
    # # record the activity log anyway
    # print('\n\n-----Invoking activity_log microservice-----')
    # invoke_http(activity_log_URL, method="POST", json=order_result)
    # print("\nOrder sent to activity log.\n")
    # # - reply from the invocation is not used;
    # # continue even if this invocation fails

    # # Check the order result; if a failure, send it to the error microservice.
    # code = order_result["code"]
    # if code not in range(200, 300):

    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as order fails-----')
    #     invoke_http(error_URL, method="POST", json=order_result)
    #     # - reply from the invocation is not used; 
    #     # continue even if this invocation fails
    #     print("Order status ({:d}) sent to the error microservice:".format(
    #         code), order_result)

    #     # 7. Return error
    #     return {
    #         "code": 500,
    #         "data": {"order_result": order_result},
    #         "message": "Order creation failure sent for error handling."
    #     }

    # # 5. Send new order to shipping
    # # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')
    # shipping_result = invoke_http(
    #     shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')

    # # Check the shipping result; 
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):

    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as shipping fails-----')
    #     invoke_http(error_URL, method="POST", json=shipping_result)
    #     print("Shipping status ({:d}) sent to the error microservice:".format(
    #         code), shipping_result)

    #     # 7. Return error
    #     return {
    #         "code": 400,
    #         "data": {
    #             "order_result": order_result,
    #             "shipping_result": shipping_result
    #         },
    #         "message": "Simulated shipping record error sent for error handling."
    #     }

    # # 7. Return created order, shipping record
    # return {
    #     "code": 201,
    #     "data": {
    #         "order_result": order_result,
    #         "shipping_result": shipping_result
    #     }
    # }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for booking an appointment...")
    app.run(host="0.0.0.0", port=5100, debug=True)