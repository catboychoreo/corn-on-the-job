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
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE (job_title LIKE ? OR company LIKE ?) AND approved=1",
            (
                job_query,
                job_query,
            ),
        )
    else:
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE approved=1"
        )

    data = cursor.fetchall()
    return render_template("studenthome.html", data=data)


@app.route("/student/apply/<int:job_id>")
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
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE (job_title LIKE ? OR company LIKE ?) AND approved=1",
            (
                job_query,
                job_query,
            ),
        )
    else:
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE approved=1"
        )

    data = cursor.fetchall()
    return render_template("employerhome.html", data=data)


@app.route("/employer/post")
def go_employ():
    return render_template("employerpost.html")


@app.route("/employer/post", methods=["POST"])
def employer_post():
    job_title = request.form.get("job-title")
    job_desc = request.form.get("job-description")
    company = request.form.get("company")
    logo_file = request.files["logo"]
    logo_file.save("static/images/" + logo_file.filename)

    cursor = get_db().execute(
        "INSERT INTO jobs (job_title,description,company,logo) VALUES (?,?,?,?)",
        (
            job_title,
            job_desc,
            company,
            logo_file.filename,
        ),
    )

    get_db().commit()
    return render_template("employerpost.html")


@app.route("/admin")
def admin_home():
    job_query = request.args.get("query")

    if job_query:
        job_query = job_query + "%"
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE (job_title LIKE ? OR company LIKE ?) AND approved=1",
            (
                job_query,
                job_query,
            ),
        )
    else:
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE approved=1"
        )

    data = cursor.fetchall()
    return render_template("adminhome.html", data=data)


@app.route("/admin/delete", methods=["POST"])
def delete_job():
    post_id = request.form.get("post-id")

    if post_id:
        cursor = get_db().execute(
            "DELETE FROM jobs WHERE id=?",
            (post_id,),
        )

        if cursor.rowcount > 0:
            get_db().commit()
            print("Job deleted succesfully!")
        else:
            print("uh oh...")
    else:
        print("no job id!")

    return redirect("/admin")


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
    elif username == "admin" and password == "admin":
        return redirect("/admin")
    else:
        return redirect("/signin")


app.run()
