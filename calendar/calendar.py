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

@app.route("/calendar")
def getTimeslotID():
    # Fetch all timeslots from the Calendar table
    calendar = Calendar.query.all()

    if calendar:
        # Return a JSON response if calendar items exist
        timeslots = [{"TimeslotID": item.TimeslotID, "TimeBegin": str(item.TimeBegin), "TimeEnd": str(item.TimeEnd)} for item in calendar]
        return jsonify({
            "code": 200,
            "data": {"Timeslots": timeslots}
        })
    else:
        # Return a 404 error if no calendar items are found
        return jsonify({
            "code": 404,
            "message": "No timeslots found."
        }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)