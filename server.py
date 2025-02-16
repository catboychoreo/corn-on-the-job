from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def student_home():
    return render_template("studenthome.html")

@app.route("/apply")
def student_apply():
    return render_template("studentapply.html")

@app.route("/signin")
def sign_in():
    return render_template("signin.html")

app.run()