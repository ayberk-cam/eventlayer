from flask import Flask, flash, current_app, render_template, redirect, url_for, request, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from datetime import datetime
from functools import wraps
from classes import Student,StudentClub,Event,Member
from forms import StudentRegisterForm, ClubRegisterForm, LoginForm, EventForm
from database import Database

POSTGRESQL_URI = "postgres://vtbswxdz:PkO0W-JAq4-2eajiIxJ8rcuzk2EqnZ7c@rogue.db.elephantsql.com:5432/vtbswxdz"
db = Database(POSTGRESQL_URI)

app = Flask(__name__)
app.config["db"] = db
app.secret_key = 'eventlayer'

def studentlogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "studentlogged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view this page.","danger")
            return redirect(url_for("studentlogin_page"))
    return decorated_function

def clublogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "clublogged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view this page.","danger")
            return redirect(url_for("clublogin_page"))
    return decorated_function

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/studentregister",methods=["GET", "POST"])
def studentregister_page():
    form = StudentRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        student_name = form.name.data
        student_surname = form.surname.data
        student_department = form.department.data
        student_username = form.username.data
        student_email = form.email.data
        student_password = sha256_crypt.encrypt(form.password.data)
        student = Student(student_name,student_surname,student_department,student_username,student_email,student_password)
        db.registerStudent(student)
        flash("You have successfully registered.","success")
        return redirect(url_for("studentlogin_page"))
    else:
        return render_template("studentregister.html", form=form)

@app.route("/clubregister",methods=["GET", "POST"])  
def clubregister_page():
    form = ClubRegisterForm(request.form)
    if request.method == "POST" and form.validate():
        studentclub_name = form.name.data
        studentclub_profession = form.profession.data
        studentclub_username = form.username.data
        studentclub_email = form.email.data
        studentclub_password = sha256_crypt.encrypt(form.password.data)
        studentclub = StudentClub(studentclub_name,studentclub_profession,studentclub_username,studentclub_email,studentclub_password)
        db.registerStudentClub(studentclub)
        flash("You have successfully registered.","success")
        return redirect(url_for("clublogin_page"))
    else:
        return render_template("clubregister.html", form=form)

@app.route("/login")   
def login_page():
    return render_template("login.html")

@app.route("/studentlogin",methods=["GET", "POST"]) 
def studentlogin_page():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        student_id = db.getStudentId(username)
        if student_id != None:
            student = Student(username=username,password=password,name=None,surname=None,email=None,department=None)
            student_ = db.getStudent(student.username)
            real_password = student_.password
            if sha256_crypt.verify(password,real_password):
                flash("You have successfully logged in.","success")
                session["studentlogged_in"] = True
                session["username"] = username
                return redirect(url_for("studentlistevents_page"))
            else:
                flash("Wrong password","danger")
                return redirect(url_for("studentlogin_page"))
        else:
            flash("Wrong username","danger")
            return redirect(url_for("studentlogin_page"))
    else:
        return render_template("studentlogin.html", form = form)

@app.route("/clublogin",methods=["GET", "POST"]) 
def clublogin_page():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        studentclub_id = db.getClubId(username)
        if studentclub_id != None:
            studentclub = StudentClub(club_username=username,club_password=password,club_name=None,club_profession=None,club_email=None)
            studentclub_ = db.getStudentClub(studentclub.club_username)
            real_password = studentclub_.club_password
            if sha256_crypt.verify(password,real_password):
                flash("You have successfully logged in.","success")
                session["clublogged_in"] = True
                session["username"] = username
                return redirect(url_for("clubmyevents_page"))
            else:
                flash("Wrong password","danger")
                return redirect(url_for("clublogin_page"))
        else:
            flash("Wrong username","danger")
            return redirect(url_for("clublogin_page"))
    else:
        return render_template("clublogin.html", form = form)

@app.route("/studentlistevents") 
@studentlogin_required
def studentlistevents_page():
    events = db.getAllEvents()
    return render_template("studentlistevents.html", events = events)

@app.route("/studentclubs")
@studentlogin_required
def student_clubs_page():
    clubs = db.getAllClubs()
    return render_template("student_clubs.html", clubs = clubs)

@app.route("/member/<string:id>")
@studentlogin_required
def member_page(id):
    student_id = db.getStudentId(session["username"])
    club_id = id
    check = db.getStudentClubIdfromMember(club_id)
    if check != student_id:
        member = Member(student_id=student_id,club_id=club_id)
        db.beMember(member)
        flash("Congratulations! You are now a member.")
        return redirect(url_for("student_clubs_page"))
    else:
        flash("You are a member already.")
        return redirect(url_for("student_clubs_page"))

@app.route("/clubaddevent",methods=["GET", "POST"]) 
@clublogin_required
def clubaddevent_page():
    form = EventForm(request.form)
    if request.method == "POST" and form.validate():
        eventname = form.eventname.data
        eventdate = form.date.data
        eventime = form.time.data
        eventplace = form.place.data
        eventcontent = form.content.data
        studentclub_id = db.getClubId(session["username"])
        studentclub_name = db.getClubName(session["username"])
        event = Event(id=None,club_id=studentclub_id,club_name=studentclub_name,event_name=eventname,event_date=eventdate,event_time=eventime,event_place=eventplace,event_content=eventcontent)
        db.addEvent(event)
        flash("You have successfully added event.","success")
        return redirect(url_for("clubmyevents_page"))
    else:
        return render_template("clubaddevent.html", form = form)

@app.route("/clublistevents")
@clublogin_required
def clubmyevents_page():
    studentclub_id = db.getClubId(session["username"])
    events = db.getEvents(studentclub_id)
    return render_template("clubmyevents.html", events = events)

@app.route("/clubevent/<string:id>") 
def clubevent_page(id):
    event = db.getEvent(id)
    return render_template("clubevent.html", event = event)

@app.route("/clubmembers")
@clublogin_required
def clubmembers_page():
    studentclub_id = db.getClubId(session["username"])
    student_ids = db.getMember(studentclub_id)
    printed_members = []
    for list in student_ids:
        for member in list:
            members = db.getStudentforMember(member)
            printed_members.append(members)
    print(printed_members)
    return render_template("clubmembers.html", printed_members = printed_members)

@app.route("/delete/<string:id>") 
@clublogin_required
def clubdelete_page(id):
    studentclub_id = db.getClubId(session["username"])
    event_club_id = db.getStudentClubIdfromEvent(id)
    if studentclub_id == event_club_id:
        db.deleteEvent(id)
        return redirect(url_for("clubmyevents_page"))
    else:
        flash("There is no Event or You do not have authorization")
        return redirect(url_for("clubmyevents_page"))

@app.route("/update/<string:id>",methods=["GET", "POST"]) 
@clublogin_required
def clubupdate_page(id):
    form = EventForm(request.form)
    if request.method == "POST" and form.validate():
        eventname = form.eventname.data
        eventdate = form.date.data
        eventime = form.time.data
        eventplace = form.place.data
        eventcontent = form.content.data
        studentclub_id = db.getClubId(session["username"])
        studentclub_name = db.getClubName(session["username"])
        event = Event(id = id,club_id=studentclub_id,club_name=studentclub_name,event_name=eventname,event_date=eventdate,event_time=eventime,event_place=eventplace,event_content=eventcontent)
        db.updateEvent(event)
        flash("You have successfully updated event.","success")
        return redirect(url_for("clubmyevents_page"))
    else:
        return render_template("clubupdate.html", form = form)

@app.route("/logout") 
def logout_page():
    session.clear()
    return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run()