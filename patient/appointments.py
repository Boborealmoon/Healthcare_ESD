from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ

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

@app.route('/appointments/<string:PatientID>')
def get_appointment_by_ID(PatientID):
    appointmentlist = db.session.scalars(db.select(appointments).filter_by(PatientID=PatientID))

    if appointmentlist:
        appointments_data = [appointment.json() for appointment in appointmentlist]
        if len(appointments_data) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "appointments": appointments_data
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

# @app.route("/book/<string:isbn13>", methods=['POST'])
# def create_book(isbn13):
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
# #         ), 500


#     return jsonify(
#         {
#             "code": 201,
#             "data": book.json()
#         }
#     ), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
