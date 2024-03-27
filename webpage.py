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
    return redirect(url_for('home'))
    # file='index.html'
    # return render_template(file)

@app.route('/')
def home():
    return render_template('index.html')

# Claims route
# @app.route('/claims')
# def about():
#     return render_template('claims.html')

# Create_claims route
# @app.route('/claims')
# def about():
#     return render_template('create_claims.html')


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
