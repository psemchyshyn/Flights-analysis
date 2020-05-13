'''
FligthsDetector
Pavlo Semchyshyn
'''


from flask import Flask, redirect, url_for, render_template


flask_app = Flask(__name__)

@flask_app.route("/")
def start():
    return redirect(url_for("home"))

@flask_app.route("/home")
def home():
    return render_template("home.html")

@flask_app.route("/menu")
def menu():
    return render_template("menu.html")

@flask_app.route("/about")
def about():
    return render_template("about.html")

