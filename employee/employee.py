from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

# from flasgger import Swagger

#constructor
app = Flask(__name__)

#conncecting to SQLAlchemy: 
#The SQLAlchemy Database URI format is: dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL', 'mysql+mysqlconnector://root@localhost:3306/employees')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# export dbURL=mysql+mysqlconnector://root:root@localhost:8889/employees

#assigning connection to db -> Storing it in variable db
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employees'
    EmployeeID = db.Column(db.String(2), primary_key=True)
    EmployeeName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)

    def __init__(self, EmployeeID, EmployeeName, Email):
        self.EmployeeID = EmployeeID
        self.EmployeeName = EmployeeName
        self.Email = Email

    def json(self):
        return {
            "EmployeeID": self.EmployeeID,
            "EmployeeName": self.EmployeeName,
            "Email": self.Email
        }


@app.route("/employees")
def get_all():
    #retrive all records
    employeeList = Employee.query.all()


    if len(employeeList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "employees": [employee.json() for employee in employeeList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no employees."
        }
    ), 404


@app.route("/employees/<string:EmployeeID>")
def find_by_ID(EmployeeID):
    employee = Employee.query.filter_by(EmployeeID=EmployeeID).first()

    if employee:
        return jsonify(
            {
                "code": 200,
                "data": employee.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": " {EmployeeID} not found."
        }
    ), 404

@app.route("/employees/email/<int:EmployeeID>")
def getPatientEmail(EmployeeID):
    employee = Employee.query.filter_by(EmployeeID=EmployeeID).first()

    if employee:
        return jsonify(
            {
                "code": 200,
                "data": {"Email": employee.Email}
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": " Employee not found."
        }
    ), 404

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
