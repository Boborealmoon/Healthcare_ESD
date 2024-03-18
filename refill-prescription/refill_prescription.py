from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

employees_url = "http://localhost:5003/employee"
inventory_url = "http://localhost:5004/inventory"
order_url = "http://localhost:5005/create_order"

# -----------------
@app.route("/refill_prescription", methods=['GET'])
def check_inventory_threshold():
    # Make a GET request to the /inventory endpoint to get all inventory items
    response = requests.get(inventory_url)
    
    # Check if the request was successful
    if response.status_code in range(199,399):
        inventory_data = response.json()["data"]["inventory"]
        items_below_threshold = []
        orders = []

        # Fetch the last OrderID from the database
        lastOrderID = db.session.query(func.max(Order.OrderID)).scalar()
        newOrderID = 901 if lastOrderID is None else lastOrderID + 1

        for item in inventory_data:
            # Check if ProductQty is less than Threshold
            if item["ProductQty"] < item["Threshold"]:
                items_below_threshold.append({
                    "ProductID" : item["ProductID"],
                    "ProductName": item["ProductName"],
                    "ProductQty": item["ProductQty"],
                    "SupplierID": item["SupplierID"],
                    "SupplierContactEmail": item["SupplierContactEmail"]
                })

        for item in items_below_threshold:
            order_data = {
                "OrderID": newOrderID,
                "UnitsOrdered": 50,
                "OrderDate": "2024-06-07",
                "ProductID": item["ProductID"],
                "ProductName": item["ProductName"],
                "ProductQty": item["ProductQty"],
                "SupplierID": item["SupplierID"],
                "SupplierContactEmail": item["SupplierContactEmail"]
            }
            
            print('\n-----Invoking order microservice-----')
            order_result = invoke_http(order_url, method='POST', json=order_data)
            print('order_result:', order_result)
            if order_result.get("code") not in range(200, 300):

                print(f"Failed to create order for {item['ProductName']}")
            orders.append(order_data)
        return jsonify({"status": "success", "items_below_threshold": order_result})

    else:
        # Handle the case where the request was not successful
        print("Failed to fetch inventory data")
        return None

if __name__ == "__main__":
    print("success")
    app.run(host="0.0.0.0", port=5100, debug=True)
