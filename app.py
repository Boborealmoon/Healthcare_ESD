from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ

from flasgger import Swagger

#constructor
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
