from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL','mysql+mysqlconnector://root:root@localhost:8889/appointments')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# export dbURL=mysql+mysqlconnector://root:root@localhost:8889/appointments

db = SQLAlchemy(app)

class appointments(db.Model):
    __tablename__ = 'appointments'
    AppointmentID = db.Column(db.Integer,primary_key=True)
    AppointmentDate = db.Column(db.Date, nullable=False)
    TimeslotID = db.Column(db.Integer, nullable=False)
    EmployeeID = db.Column(db.String(2), nullable=False)
    PatientID = db.Column(db.String(3), nullable=False)
    PatientName = db.Column(db.String(50), nullable=False)
    Claimed = db.Column(db.Boolean, nullable=False)

    def __init__(self, AppointmentID, AppointmentDate, TimeslotID, EmployeeID, PatientID, PatientName, Claimed):
        self.AppointmentID = AppointmentID
        self.AppointmentDate = AppointmentDate
        self.TimeslotID = TimeslotID
        self.EmployeeID = EmployeeID
        self.PatientID = PatientID
        self.PatientName = PatientName
        self.Claimed = Claimed

    def json(self):
        return {"AppointmentID": self.AppointmentID, "AppointmentDate": self.AppointmentDate, "TimeslotID": self.TimeslotID, "EmployeeID": self.EmployeeID, "PatientID": self.PatientID, "PatientName":self.PatientName, "Claimed":self.Claimed}

@app.route('/appointments')
def get_avail_appointment():
    appointmentlist = db.session.scalars(db.select(appointments))
    timeslots = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    if appointmentlist:
        appointments_data = [appointment.json() for appointment in appointmentlist]
        today = date.today() #To get todays date
        appointments_booked = [] #To consolidate all appointments booked on the date
        timeslots_booked = [] #To consolidate all timeslots booked on the date
        
        for appointment in appointments_data:
            if appointment["AppointmentDate"] == today:
                appointments_booked.append(appointment)

        for appointment in appointments_booked:
            timeslots_booked.append(appointment["TimeslotID"])

        for slot in timeslots_booked:
            if slot in timeslots:
                timeslots.remove(slot)

        if len(timeslots) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "appointments": timeslots
                    },
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": f"No appointments made today."
                }
            ), 404

@app.route('/appointments/<string:PatientID>')
def get_appointment_by_ID(PatientID):
    appointmentlist = db.session.scalars(db.select(appointments).filter_by(PatientID=PatientID))

    if appointmentlist:
        appointments_data = [appointment.json() for appointment in appointmentlist]
        appointments_not_claimed = []
        for appointment in appointments_data:
            if appointment["Claimed"] == False :
                appointments_not_claimed.append(appointment)

        if len(appointments_not_claimed) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "appointments": appointments_not_claimed
                    }
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": f"No appointments made by Patient {PatientID}."
                }
            ), 404

@app.route("/appointments", methods=['POST'])
def create_appointment():

    max_appointment_id = db.session.query(func.max(appointments.AppointmentID)).scalar()

    # Increment the max AppointmentID by 1 to determine the ID for the new appointment
    next_appointment_id = max_appointment_id + 1 if max_appointment_id is not None else 1
    
    data = request.get_json()
    
    appointmentlist = db.session.scalars(db.select(appointments).filter_by(AppointmentDate=data['AppointmentDate']))

    if appointmentlist:
        appointments_data = [appointment.json() for appointment in appointmentlist]
        appointments_booked = []
        for appointment in appointments_data:
            appointments_booked.append(appointment['TimeslotID'])
    
    if data['TimeslotID'] in appointments_booked:
        return jsonify(
            {
                "code": 400,
                "message": f"Error booking appointment, Unavailable booking"
            }
        ),400

    new_appointment = appointments(
        AppointmentID = next_appointment_id,
        AppointmentDate=data['AppointmentDate'],
        TimeslotID=data['TimeslotID'],
        EmployeeID=data['EmployeeID'],
        PatientID=data['PatientID'], 
        PatientName=data['PatientName'],
        Claimed=data['Claimed'])

    
    try:
        db.session.add(new_appointment)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "appointment": "ok"
                },
                "message": "An error occurred creating the appointment."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": new_appointment.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
