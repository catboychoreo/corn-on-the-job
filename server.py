from flask import Flask, render_template, request, redirect, g, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename # <-- And this

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "Bila4EkX2X"
app.config["UPLOAD_FOLDER"] = "static/resumes"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# gets the database from sql
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("main.db")
    return db

# establishes the student home page 
@app.route("/student")
def student_home():
    job_query = request.args.get("query")

    # makes search bar functional
    if job_query:
        job_query = "%" + job_query + "%"
        
        # shows the job titles/company names that match what the user has entered as a query
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE (job_title LIKE ? OR company LIKE ?) AND approved=1",
            (
                job_query,
                job_query,
            ),
        )
    else:
        # returns normal homepage when no query is entered
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE approved=1"
        )

    data = cursor.fetchall()
    return render_template("studenthome.html", data=data)

# creates different application pages for different job listings based off of their ids
@app.route("/student/apply/<int:job_id>")
def student_apply(job_id):
    cursor = get_db().execute(
        "SELECT id,job_title,description,company FROM JOBS WHERE id=?", (job_id,)
    )
    data = cursor.fetchone()
    return render_template("studentapply.html", data=data)

@app.route("/student/apply/submit/<int:job_id>", methods=["POST"])
def submit_application(job_id):
    if "user_id" not in session or session["user_type"] != "student":
        return redirect("/signin")
    
    user_id = session["user_id"]

    experience = request.form.get("applicant_experience")
    phone = request.form.get("phone_number")
    email = request.form.get("email")

    # default to None if no resume is uploaded
    resume_filename = None
    if "resume" in request.files and request.files["resume"].filename != "":
        resume_file = request.files["resume"]
        # secure the filename to prevent security issues
        filename = secure_filename(resume_file.filename)
        resume_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        resume_filename = filename

    db = get_db()
    db.execute(
        """
        INSERT INTO APPLICATIONS 
        (user_id, job_id, experience_summary, phone_number, contact_email, resume_filename) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, job_id, experience, phone, email, resume_filename)
    )
    db.commit()

    return redirect("/student")

@app.route("/student/myapplications")
def my_applications():
    if "user_id" not in session or session["user_type"] != "student":
        return redirect("/signin")

    user_id = session["user_id"]
    
    cursor = get_db().execute(
        """
        SELECT j.id, j.job_title, j.description, j.company, j.logo
        FROM JOBS j
        JOIN APPLICATIONS a ON j.id = a.job_id
        WHERE a.user_id = ?
        """,
        (user_id,)
    )
    data = cursor.fetchall()
    
    return render_template("myapplications.html", data=data)


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

# creates posting page for employer
@app.route("/employer/post", methods=["POST"])
def employer_post():
    job_title = request.form.get("job-title")
    job_desc = request.form.get("job-description")
    company = request.form.get("company")
    user_id = session.get("user_id")

    # creates logo files for companies
    if "logo" in request.files and request.files["logo"].filename: 
        logo_file = request.files["logo"]
        logo_file.save("static/images/" + logo_file.filename)
        
        file_name = logo_file.filename
        
    # if there is no logo, replace logo w/ placeholder image
    else:
        file_name = "placeholder.webp"

    # adds employer information to the database
    cursor = get_db().execute(
        "INSERT INTO jobs (job_title, description, company, logo, user_id) VALUES (?, ?, ?, ?, ?)",
        (
            job_title,
            job_desc,
            company,
            file_name,
            user_id,
        ),
    )
    get_db().commit()
    return render_template("employerpost.html")

@app.route("/employer/mypostings")
def my_postings():
    if "user_id" not in session or session["user_type"] != "employer":
        return redirect("/signin")

    user_id = session["user_id"]

    cursor = get_db().execute(
        "SELECT id, job_title, description, company, logo, approved FROM JOBS WHERE user_id = ?",
        (user_id,)
    )
    data = cursor.fetchall()

    return render_template("mypostings.html", data=data)


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

# deletes job posting from the database (admin side only)
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

# works the same as the admin home but displays UNAPPROVED posts instead of approved
@app.route("/admin/review")
def admin_review():
    job_query = request.args.get("query")

    if job_query:
        job_query = job_query + "%"
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE (job_title LIKE ? OR company LIKE ?) AND approved=0",
            (
                job_query,
                job_query,
            ),
        )
    else:
        cursor = get_db().execute(
            "SELECT id,job_title,description,company,logo FROM JOBS WHERE approved=0"
        )

    data = cursor.fetchall()
    return render_template("adminapprove.html", data=data)    

# will deny the post and delete it from the database
@app.route("/admin/deny", methods=["POST"])
def deny_job():
    post_id = request.form.get("deny-id")

    if post_id:
        cursor = get_db().execute(
            "DELETE FROM jobs WHERE id=?", (post_id,))
        if cursor.rowcount > 0:
            get_db().commit()
            print("Job deleted succesfully!")
        else:
            print("uh oh...")
    else:
        print("no job id!")

    return redirect("/admin/review")

# approves the job and updates database to make the post approved
@app.route("/admin/approve", methods=["POST"])
def approve_job():
    post_id = request.form.get("approve-id")

    cursor = get_db().execute("UPDATE jobs SET approved=1 WHERE id=?", (post_id,),)
    get_db().commit()

    return redirect("/admin/review")


@app.route("/")
def go_sign():
    return redirect("/signin")


@app.route("/signin")
def sign_in():
    return render_template("signin.html")

# sets usernames and passwords for student, admin and employer accounts
@app.route("/signin", methods=["GET", "POST"])
def get_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        db = get_db()
        user = db.execute("SELECT * FROM USERS WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user[2], password):  # user[2] is the password column
            session["user_id"] = user[0]  # user[0] is the id column
            session["user_type"] = user[3] # user[3] is the user_type column

            if session["user_type"] == "student":
                return redirect("/student")
            elif session["user_type"] == "employer":
                return redirect("/employer")
            elif session["user_type"] == "admin":
                return redirect("/admin")
        else:

            return redirect("/signin")
    
    return render_template("signin.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_type = request.form.get("user_type")

        assert user_type in ["employer", "student"]

        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO USERS (username, password, user_type) VALUES (?, ?, ?)",
                (username, hashed_password, user_type),
            )
            db.commit()
        except sqlite3.IntegrityError:
            return "Username already taken. Please go back and try another."

        return redirect("/signin")

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear() 
    return redirect("/signin")

app.run()
