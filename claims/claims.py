from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class claims(db.Model):
    __tablename__ = 'claims'
    ClaimID = db.Column(db.String(3), primary_key=True)
    StatusOfClaims = db.Column(db.String(50), nullable=False)
    AppointmentID = db.Column(db.Integer, nullable=False)