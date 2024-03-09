from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

employees_url = "http://localhost:5003/employee"
inventory_url = "http://localhost:5004/inventory"
order_url = "http://localhost:5005/order"


