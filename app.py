from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import environ

from flasgger import Swagger

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("./templates/index.html")

# Fixed route function to correctly capture the input
@app.route("/<name>")
def routing(name):
    return redirect(url_for("user", name=name))

# New route to handle redirection
@app.route("/user/<name>")
def user(name):
    return f"Welcome, {name}!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
