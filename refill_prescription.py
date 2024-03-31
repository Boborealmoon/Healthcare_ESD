from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from datetime import date

import requests
from invokes import invoke_http

import os, sys
from os import environ

import pika
import json
import amqp_connection
import sys

app = Flask(__name__)
CORS(app)

employees_url = "http://kong:8000/api/v1/employees"   
inventory_url = "http://kong:8000/api/v1/inventory"   
order_url = "http://kong:8000/api/v1/orders"   
email_service_url = "http://kong:8000/api/v1/emailservice"


exchangename = "clinic_topic"  # exchange name
exchangetype = "topic"  # use a 'topic' exchange to enable interaction

# create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection()
channel = connection.channel()

# if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

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

        message = json.dumps(order_result)

        if order_result.get("code") not in range(200, 300):
            #changes made#
            print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')           
            channel.basic_publish(exchange=exchangename, routing_key="order.error",
                                  body=message, properties=pika.BasicProperties(delivery_mode=2))
            print("\nOrder Creation Failure ({:d}) published to the RabbitMQ Exchange:".format(
                order_result.get("code")), order_result)

            # Return error
            return {
                "code": 500,
                "data": {"order_result": order_result},
                "message": "Order creation failure sent for error handling."
            }
        
        else:
            print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')                 
            channel.basic_publish(exchange=exchangename, routing_key="order.info", 
            body=message)
        
            print("\nOrder published to RabbitMQ Exchange.\n")
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
            employee_email = invoke_http(employees_url + f'/email/21')
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
    
    return jsonify({"status": "success", "order": order_result},201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
