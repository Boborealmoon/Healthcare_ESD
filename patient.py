from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
# from flasgger import Swagger

#constructor
app = Flask(__name__)
CORS(app)
#conncecting to SQLAlchemy: 
#The SQLAlchemy Database URI format is: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:8889/patients'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#assigning connection to db -> Storing it in variable db
db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__ = 'patients'
    PatientID = db.Column(db.String(3), primary_key=True)
    PatientName = db.Column(db.String(50), nullable=False)
    ContactNo = db.Column(db.String(8), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    NRIC = db.Column(db.String(9), nullable=False)

    # Initialize Patient object
    def __init__(self, PatientID, PatientName, ContactNo, Email, NRIC):
        self.PatientID = PatientID
        self.PatientName = PatientName
        self.ContactNo = ContactNo
        self.Email = Email
        self.NRIC = NRIC

    # Represent Patient object as a dictionary
    def json(self):
        return {
            "PatientID": self.PatientID,
            "PatientName": self.PatientName,
            "ContactNo": self.ContactNo,
            "Email": self.Email,
            "NRIC": self.NRIC
        }

@app.route("/patient")
def get_all():
    #retrive all records
    patientList = Patient.query.all()

    if len(patientList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "patients": [patient.json() for patient in patientList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no patients."
        }
    ), 404


@app.route("/patient/ID/<string:PatientID>")
def find_by_ID(PatientID):

    patient = Patient.query.filter_by(PatientID=PatientID).first()

    if patient:
        return jsonify(
            {
                "code": 200,
                "data": patient.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": " {PatientID} not found."
        }
    ), 404

@app.route("/patient/email/<string:PatientID>")
def getPatientEmail(PatientID):
    patient = Patient.query.filter_by(PatientID=PatientID).first()

    if patient:
        return jsonify({
            "code": 200,
            "data": {"Email": patient.Email}
        })
    return jsonify({
        "code": 404,
        "message": "Patient not found."
    }), 404

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
