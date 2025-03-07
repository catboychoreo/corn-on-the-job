from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("main.db")
    return db

@app.route("/student")
def student_home():
    cursor = get_db().execute("SELECT id,job_title,description,company FROM JOBS")
    data = cursor.fetchall()
    return render_template("studenthome.html", data = data)

@app.route("/apply")
def student_apply():
    return render_template("studentapply.html")

@app.route("/")
def go_sign():
    return redirect("/signin")

@app.route("/signin")
def sign_in():
    return render_template("signin.html")

@app.route("/signin", methods = ["POST"])
def get_in():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "student" and password == "student":
        return redirect("/student")
    else:
        return redirect("/signin")

app.run()