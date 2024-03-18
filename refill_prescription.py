from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from datetime import date

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

employees_url = "http://localhost:5003/employees"
inventory_url = "http://localhost:5004/inventory"
order_url = "http://localhost:5005/create_order"
activitylog_url = "http://localhost:5007/activity_log"
error_url = "http://localhost:5008/error"
email_service_url = "http://localhost:5010/email_service"

# -----------------
@app.route("/refill_prescription", methods=['GET'])
def refill_prescription():
    # Make a GET request to the /inventory endpoint to get all inventory items
    print('\n-----Invoking inventory microservice-----')
    inventory_result = invoke_http(inventory_url)
    print('inventory_result:', inventory_result)
    
    # Check if the request was successful
    inventory_data = inventory_result["data"]["inventory"]
    items_below_threshold = []
    orders = []

    for item in inventory_data:
        # Check if ProductQty is less than Threshold
        if item["ProductQty"] < item["Threshold"]:
            items_below_threshold.append({
                "ProductID" : item["ProductID"],
                "ProductName": item["ProductName"],
                "ProductQty": item["ProductQty"],
                "SupplierID": item["SupplierID"],
                "SupplierContactEmail": item["SupplierContactEmail"],
                "UnitsToOrder": item["UnitsToOrder"]
            })

    for item in items_below_threshold:
        today = str(date.today())
        order_data = {
            "UnitsOrdered": item["UnitsToOrder"],
            "OrderDate": today,
            "ProductID": item["ProductID"],
            "ProductName": item["ProductName"],
            "ProductQty": item["ProductQty"],
            "SupplierID": item["SupplierID"],
            "SupplierContactEmail": item["SupplierContactEmail"]
        }
        
        print('\n-----Invoking order microservice to create order-----')
        order_result = invoke_http(order_url, method='POST', json=order_data)
        print('order_result:', order_result)

        print('\n-----Invoking activity_log microservice-----')
        invoke_http(activitylog_url, method="POST", json=order_result)
        print('\nOrder sent to activity log.\n')

        if order_result.get("code") not in range(200, 300):
            print('\n\n-----Invoking error microservice as order fails-----')
            invoke_http(error_url, method="POST", json=order_result)
            # - reply from the invocation is not used; 
            # continue even if this invocation fails
            print("Order Creation status sent to the error microservice:".format(
                order_result.get("code")), order_result)

            # Return error
            return {
                "code": 500,
                "data": {"order_result": order_result},
                "message": "Order creation failure sent for error handling."
            }
        orders.append(order_data)

        vendor_email = item["SupplierContactEmail"]

        email_data = {
            "recipient_email": vendor_email,
            "subject": "Order Confirmation",
            "message_body": f"Dear Sir/Mdm,\n\nClinic has placed an order.\n\nThank you!"
        }

        print('\n\n-----Invoking email microservice-----')
        email_result = invoke_http(email_service_url, method='POST', json=email_data)
        print(email_result)

    
    print('\n-----Invoking employee microservice-----')
    employee_email = invoke_http(employees_url)
    print('employee_email:', employee_email)

    
    clinic_email = employee_email['data']['Email']

    email_data = {
            "recipient_email": clinic_email,
            "subject": "Order Confirmation",
            "message_body": f"Dear Sir/Mdm,\n\nClinic has placed an order. \n\n\n\nThank you!"
        }

    print('\n\n-----Invoking email microservice-----')
    email_result = invoke_http(email_service_url, method='POST', json=email_data)
    print(email_result)
    
    return jsonify({"status": "success", "order": order_result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
