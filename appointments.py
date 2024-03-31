from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@localhost:8889/appointments'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

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
        return {
            "AppointmentID": self.AppointmentID, 
            "AppointmentDate": self.AppointmentDate.strftime('%A, %Y-%m-%d'), 
            "TimeslotID": self.TimeslotID, 
            "EmployeeID": self.EmployeeID, 
            "PatientID": self.PatientID, 
            "PatientName":self.PatientName, 
            "Claimed":self.Claimed}

# Modify the Flask function to return timeslots as objects with ID and time
@app.route('/appointments')
def get_avail_appointment():
    selected_date = request.args.get('selected_date')  # Get the selected date from the query parameters

    if not selected_date:
        return jsonify({"error": "No selected date provided"}), 400

    appointmentlist = db.session.query(appointments).filter(appointments.AppointmentDate == selected_date).all()
    
    timeslots = [
        {"id": 1, "time": "09:00 AM"},
        {"id": 2, "time": "09:30 AM"},
        {"id": 3, "time": "10:00 AM"},
        {"id": 4, "time": "10:30 AM"},
        {"id": 5, "time": "11:00 AM"},
        {"id": 6, "time": "11:30 AM"},
        {"id": 7, "time": "12:00 PM"},
        {"id": 8, "time": "13:30 PM"},
        {"id": 9, "time": "14:00 PM"},
        {"id": 10, "time": "14:30 PM"},
        {"id": 11, "time": "15:00 PM"},
        {"id": 12, "time": "15:30 PM"},
        {"id": 13, "time": "16:00 PM"},
        {"id": 14, "time": "16:30 PM"},
    ]
    if appointmentlist:
        appointments_data = [appointment.json() for appointment in appointmentlist]
        appointments_booked = []
        timeslots_booked = []

        for appointment in appointments_data:
            appointments_booked.append(appointment)

        for appointment in appointments_booked:
            timeslots_booked.append(appointment["TimeslotID"])

        available_timeslots = [slot for slot in timeslots if slot["id"] not in timeslots_booked]

        print(available_timeslots)
        
        if len(available_timeslots) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "appointments": available_timeslots
                    },
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": f"No appointments available for {selected_date}."
                }
            ), 404
    else:
        # If there are no appointments for the selected date, return all timeslots
        return jsonify({
            "code": 200,
            "data": {
                "appointments": timeslots
            },
        })


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
        Claimed=False)

    
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

@app.route("/appointments/<string:PatientID>/<int:AppointmentID>", methods=['PUT'])
def update_appointment(PatientID, AppointmentID):
    data = request.get_json()
    
    # Query the appointment with the specified PatientID and AppointmentID
    appointment = appointments.query.filter_by(PatientID=PatientID, AppointmentID=AppointmentID).first()

    print(appointment)
    if appointment:
        # Update the claim status if it's present in the request data
        if 'Claimed' in data:
            appointment.Claimed = data['Claimed']

        try:
            db.session.commit()
            return jsonify({
                "code": 200,
                "data": appointment.json(),
                "message": "Appointment updated successfully."
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "message": f"Failed to update appointment: {str(e)}"
            }), 500
    else:
        return jsonify({
            "code": 404,
            "message": f"Appointment with PatientID {PatientID} and AppointmentID {AppointmentID} not found."
        }), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
