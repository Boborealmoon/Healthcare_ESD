from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

book_URL = "http://localhost:5000/book"
order_URL = "http://localhost:5001/order"
shipping_record_URL = "http://localhost:5002/shipping_record"
activity_log_URL = "http://localhost:5003/activity_log"
error_URL = "http://localhost:5004/error"


appointment_URL="http://localhost:5001/appointments"
calender_URL="http://localhost:5001/calendar"
patient_URL="http://localhost:5001/patients"

