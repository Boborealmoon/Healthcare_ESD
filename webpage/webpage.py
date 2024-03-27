from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from datetime import date
from flask_cors import CORS

from flask import render_template

app = Flask(__name__, template_folder='templates')
CORS(app)



@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/home')
def home():
    abs_path='/usr/src/app/Templates/index.html'
    file='index.html'
    return render_template(file)

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# Fixed route function to correctly capture the input
# @app.route("/<name>")
# def routing(name):
#     return redirect(url_for("user", name=name))

# # New route to handle redirection
# @app.route("/user/<name>")
# def user(name):
#     return f"Welcome, {name}!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
