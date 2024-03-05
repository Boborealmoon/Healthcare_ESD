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
    patientList = db.session.scalars(db.select(patients)).all()

    if len(patientList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "patients": [patients.json() for patient in patientList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no patients."
        }
    ), 404


@app.route("/patient/<string:PatientID>")
def find_by_ID(PatientID):
    patient = db.session.scalars(
    db.select(patients).filter_by(PatientID=PatientID).
    limit(1)
    ).first()

    if book:
        return jsonify(
            {
                "code": 200,
                "data": patients.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": " {PatientID} not found."
        }
    ), 404

def getPatientEmail(PatientID):
    patient = db.session.scalars(
    db.select(patients).filter_by(PatientID=PatientID).
    limit(1)
    ).first()

    if book:
        return jsonify(
            {
                "code": 200,
                "data": patients.Email.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": " Patient not found."
        }
    ), 404

# @app.route("/patient/<string:PatientID>", methods=['POST'])
# def new_patient():

#     if (db.session.scalars(
#         db.select(Book).filter_by(isbn13=isbn13).
#         limit(1)
#         ).first()
#         ):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "Patient already exists."
#             }
#         ), 400


#     data = request.get_json()
#     book = Book(isbn13, **data)


#     try:
#         db.session.add(book)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "isbn13": isbn13
#                 },
#                 "message": "An error occurred creating the book."
#             }
#         ), 500


#     return jsonify(
#         {
#             "code": 201,
#             "data": patients.json()
#         }
#     ), 201

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
