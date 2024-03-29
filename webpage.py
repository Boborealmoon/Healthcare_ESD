from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def  home():
    index_page_load = render_template('index.html')
    return index_page_load

@app.route('/<page>')
def  routed(page):
    index_page_load = f"{page}.html"
    return render_template(index_page_load)

# @app.route('/about')
# def about():
#     return render_template('about.html')

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
