from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from flask import Flask
from flask_cors import CORS

# from flasgger import Swagger

app = Flask(__name__)
CORS(app)
    
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:8889/claims'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:8889/claims'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Claim(db.Model):
    __tablename__ = 'claims'
    ClaimID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StatusOfClaims = db.Column(db.String(50), nullable=False)
    AppointmentID = db.Column(db.Integer, nullable=False)
    PatientID = db.Column(db.String(3), nullable=False)
    
    def __init__(self, ClaimID, StatusOfClaims, AppointmentID, PatientID):
        self.ClaimID = ClaimID
        self.StatusOfClaims = StatusOfClaims
        self.AppointmentID = AppointmentID
        self.PatientID = PatientID

        
    # Represent Claim objects as a dictionary
    def json(self):
        return {
            "ClaimID": self.ClaimID,
            "StatusOfClaims": self.StatusOfClaims,
            "AppointmentID": self.AppointmentID,
            "PatientID": self.PatientID
        }

# Retrieve all claims
@app.route("/claims")
def get_all():
    claimsList = Claim.query.all()
    
    if len(claimsList):
        return jsonify(
            {
                "code": 200,
                "data":  [claims.json() for claims in claimsList]
    
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No claims have been made."
        }
    )

# Create a new claim
@app.route("/new_claim", methods=['POST'])
def new_claim():
    try:
        data = request.get_json()
        last_claim = int(db.session.query(func.max(Claim.ClaimID)).scalar())
        new_claim_id = 901 if last_claim is None else last_claim + 1
        
        claim = Claim(
            ClaimID=new_claim_id,
            StatusOfClaims=data['StatusOfClaims'],
            AppointmentID=data['AppointmentID'],
            PatientID=data['PatientID']
        )
        db.session.add(claim)
        db.session.commit()
        
        response = {
            "code": 201,
            "message": "Claim created successfully",
            "data": claim.json()
        }
        
        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": f"An error occurred submitting the claim: {str(e)}"
        }), 500
    
#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

