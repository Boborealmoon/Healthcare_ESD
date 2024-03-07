from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class appointments(db.Model):
    __tablename__ = 'appointments'
    AppointmentID = db.Column(db.Integer, primary_key=True)
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

@app.route("/appointments/<string:PatientID>", methods=['POST'])
def create_appointment(PatientID):

    # NO NEED TO CHECK IF APPOINTMENT IS MADE BEFORE ANOT, CAUSE WE ONLY RETURN AVAILABLE APPOINTMENTS
    #     if (db.session.scalars(
    #     	db.select(Book).filter_by(isbn13=isbn13).
    #     	limit(1)
    # ).first()
    # ):
    #         return jsonify(
    #             {
    #                 "code": 400,
    #                 "data": {
    #                     "isbn13": isbn13
    #                 },
    #                 "message": "Book already exists."
    #             }
    #         ), 400

    data = request.get_json()
    new_appointment = appointments(PatientID, **data)

    try:
        db.session.add(new_appointment)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "appointment": data
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
    app.run(host="0.0.0.0", port=5001, debug=True)
