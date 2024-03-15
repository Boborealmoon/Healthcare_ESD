from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

appointments_url = "http://localhost:5000/appointments"
# calendar_url = "http://localhost:5001/Clinic_calendar"
claims_url = "http://localhost:5002/claims"
# employees_url = "http://localhost:5003/employee"
# inventory_url = "http://localhost:5004/inventory"
# order_url = "http://localhost:5005/order"
patients_url = "http://localhost:5006/patient"
activitylog_url = "http://localhost:5007/activity_log"
error_url = "http://localhost:5008/error"

@app.route("/submit_claims", methods=['POST'])
def submit_claims():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
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

    # Record new claim in activity_log
    print('\n\n-----Invoking activity_log microservice-----')
    invoke_http(activitylog_URL, method="POST", json=claim_result)
    print("\nClaim sent to activity log.\n")
    
    # Check the claim_result; if a failure, send it to the error microservice.
    code = claim_result["code"]
    if code not in range(200, 300):
        
        # Inform the error microservice
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=claim_result)
        print("Claim submission status ({:d}) sent to the error microservice:".format(
            code), claim_result)

        # Return error
        return {
            "code": 500,
            "data": {"claim_result": claim_result},
            "message": "Claim submission failed."
        }

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
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.