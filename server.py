from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("main.db")
    return db


@app.route("/student")
def student_home():
    job_query = request.args.get("query")

    if job_query:
        job_query = job_query + "%"
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE job_title LIKE ? OR company LIKE ?",
            (
                job_query,
                job_query,
            ),
        )
    else:
        cursor = get_db().execute("SELECT id,job_title,description,company,logo FROM JOBS")

    data = cursor.fetchall()
    return render_template("studenthome.html", data=data)


@app.route("/apply/<int:job_id>")
def student_apply(job_id):
    cursor = get_db().execute(
        "SELECT id,job_title,description,company FROM JOBS WHERE id=?", (job_id,)
    )
    data = cursor.fetchone()
    return render_template("studentapply.html", data=data)

@app.route("/employer")
def employer_home():
    job_query = request.args.get("query")

    if job_query:
        job_query = job_query + "%"
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE job_title LIKE ? OR company LIKE ?",
            (
                job_query,
                job_query,
            ),
        )
    else:
        cursor = get_db().execute("SELECT id,job_title,description,company,logo FROM JOBS")

    data = cursor.fetchall()
    return render_template("employerhome.html", data=data)


@app.route("/")
def go_sign():
    return redirect("/signin")


@app.route("/signin")
def sign_in():
    return render_template("signin.html")


@app.route("/signin", methods=["POST"])
def get_in():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "student" and password == "student":
        return redirect("/student")
    elif username == "employer" and password == "employer":
        return redirect("/employer")
    else:
        return redirect("/signin")


app.run()
