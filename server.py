from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/student")
def student_home():
    return render_template("studenthome.html")

@app.route("/apply")
def student_apply():
    return render_template("studentapply.html")

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