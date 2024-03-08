from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

from flasgger import Swagger

#constructor
app = Flask(__name__)

#conncecting to SQLAlchemy: 
#The SQLAlchemy Database URI format is: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# export dbURL=mysql+mysqlconnector://root:root@localhost:8889/patients

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


# @app.route("/patient/new_patient", methods=['POST'])
# def new_patient():
#     data = request.get_json()

#     # Check if the Patient with the given ID already exists
#     existing_patient = Patient.query.filter_by(PatientID=data.get('PatientID')).first()

#     if existing_patient:
#         return jsonify({
#             "code": 400,
#             "data": {"PatientID": data.get('PatientID')},
#             "message": "Patient already exists."
#         }), 400

#     # Create a new Patient object
#     new_patient = Patient(
#         PatientID=data.get('PatientID'),
#         PatientName=data.get('PatientName'),
#         ContactNo=data.get('ContactNo'),
#         Email=data.get('Email'),
#         NRIC=data.get('NRIC')
#     )

#     try:
#         # Add the new patient to the database
#         db.session.add(new_patient)
#         db.session.commit()

#         return jsonify({
#             "code": 201,
#             "data": new_patient.json()
#         }), 201
#     except Exception as e:
#         return jsonify({
#             "code": 500,
#             "data": {"PatientID": data.get('PatientID')},
#             "message": "An error occurred creating the patient."
#         }), 500

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
