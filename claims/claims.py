from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Claim(db.Model):
    __tablename__ = 'claims'
    ClaimID = db.Column(db.String(3), primary_key=True)
    StatusOfClaims = db.Column(db.String(50), nullable=False)
    AppointmentID = db.Column(db.Integer, nullable=False)
    
    # Initialize Claim object
    def __init__(self, ClaimID, StatusOfClaims, AppointmentID):
        self.ClaimID = ClaimID
        self.StatusOfClaims = StatusOfClaims
        self.AppointmentID = AppointmentID
        
    # Represent Claim objects as a dictionary
    def json(self):
        return {
            "ClaimID": self.ClaimID,
            "StatusOfClaims": self.StatusOfClaims,
            "AppointmentID": self.AppointmentID
        }

# Retrieve all claims
@app.route("/claims")
def get_all():
    claimsList = Claim.query.all()
    
    if len(claimsList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "claims": [claims.json() for claims in claimsList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No claims have been made."
        }
    )

# # Find claims by ClaimID
# @app.route("/claims/<string:ClaimID>")
# def find_by_ID(ClaimID):
#     claim = Claim.query.filter_by(ClaimID = ClaimID).first()
    
#     if claim:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": claim.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Claim {ClaimID} does not exist."
#         }
#     ), 404

# Create a new claim
@app.route("/claims/<string:ClaimID>", methods=['POST'])
def new_claim(ClaimID):
    if( db.session.scalars(
        db.select(Claim).filter_by(ClaimID = ClaimID).limit(1)
).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "ClaimID": ClaimID
                },
                "message": "Claim {ClaimID} has already been made."
            }
        ), 400
        
    data = request.get_json()
    claim = Claim(ClaimID, **data)
    
    try:
        db.session.add(claim)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "ClaimID": ClaimID
                },
                "message": "An error occured submitting the claim."
            }
        ), 500
        
    return jsonify(
        {
            "code": 201,
            "data": claim.json()
        }
    ), 201
    
    
#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)