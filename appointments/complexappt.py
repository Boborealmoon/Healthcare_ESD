from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

appointments_url = "http://localhost:5000/appointments"
calendar_url = "http://localhost:5001/Clinic_calendar"
claims_url = "http://localhost:5002/claims"
employees_url = "http://localhost:5003/employee"
inventory_url = "http://localhost:5004/inventory"
order_url = "http://localhost:5005/order"
patients_url = "http://localhost:5006/patient"



