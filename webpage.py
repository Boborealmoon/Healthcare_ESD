from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from datetime import date
from flask_cors import CORS

from flask import render_template

app = Flask(__name__, template_folder='templates')
CORS(app)


# @app.route('/')
# def index():
#     return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book_appointment')
def book_appointment():
    return redirect('book_appointments.html')

@app.route('/claims')
def claims():
    # You can define logic here to render claims.html or another suitable template
    return render_template('claims.html')

@app.route('/create_claims')
def create_claims():
    # You can define logic here to render create_claims.html or another suitable template
    return render_template('create_claims.html')


# # Fixed route function to correctly capture the input
# @app.route("/<url>")
# def routing(url):
#     return redirect(url_for("user", url=url))


# # New route to handle redirection
# @app.route("/user/<name>")
# def user(name):
#     return f"Welcome, {name}!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
