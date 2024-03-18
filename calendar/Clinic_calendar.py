from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from os import environ
import calendar

from flasgger import Swagger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# export dbURL=mysql+mysqlconnector://root:root@localhost:8889/calendar

db = SQLAlchemy(app)


class Calendar(db.Model):
    __tablename__ = 'calendar'
    TimeslotID = db.Column(db.Integer, primary_key=True)
    TimeBegin = db.Column(db.Time, nullable=False)
    TimeEnd = db.Column(db.Time, nullable=False)

    def __init__(self, TimeslotID, TimeBegin, TimeEnd):
        self.TimeslotID = TimeslotID
        self.TimeBegin = TimeBegin
        self.TimeEnd = TimeEnd

    def json(self):
        return {
            "TimeslotID": self.TimeslotID,
            "TimeBegin": str(self.TimeBegin),
            "TimeEnd": str(self.TimeEnd)
        }

@app.route("/calendar/ID/<string:TimeslotID>")
def getTimeByID(TimeslotID):
    time = Calendar.query.filter_by(TimeslotID=TimeslotID).first()

    if time:
        return jsonify(
            {
                "code": 200,
                "data": time.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": " {TimeslotID} not found."
        }
    ), 404

@app.route("/calendar")
def getAllTimeSlots():
    calendar = Calendar.query.all()

    if calendar:
        timeslots = [{"TimeslotID": item.TimeslotID, "TimeBegin": str(item.TimeBegin), "TimeEnd": str(item.TimeEnd)} for item in calendar]
        return jsonify({
            "code": 200,
            "data": {"Timeslots": timeslots}
        })
    else:
        return jsonify({
            "code": 404,
            "message": "No timeslots found."
        }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
