from flask import Flask

from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from datetime import datetime, date
from wtforms_components import DateRange

class StudentRegisterForm(Form):
    name = StringField("Name", validators=[validators.DataRequired()])
    surname = StringField("Surname", validators=[validators.DataRequired()])
    department = StringField("Department", validators=[validators.DataRequired()])
    username = StringField("Username", validators=[validators.DataRequired()])
    email = StringField("E-mail", validators=[validators.DataRequired(), validators.Email(message = "Please enter a valid e-mail")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please enter a password"), 
    validators.EqualTo(fieldname="confirm",message="Passwords does not match")])
    confirm = PasswordField("Confirm Password")

class ClubRegisterForm(Form):
    name = StringField("Name", validators=[validators.DataRequired()])
    profession = SelectField('Profession', choices=[('cat', 'Culture - Art and Thinking Student Clubs'), ('sports', 'Sports Student Clubs'), ('expert', 'Expertise Student Clubs')], validators=[validators.DataRequired()])
    username = StringField("Username", validators=[validators.DataRequired()])
    email = StringField("E-mail", validators=[validators.DataRequired(), validators.Email(message = "Please enter a valid e-mail")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please enter a password"), 
    validators.EqualTo(fieldname="confirm",message="Passwords does not match")])
    confirm = PasswordField("Confirm Password")

class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")

class EventForm(Form):
    eventname = StringField("Name of the Event", validators=[validators.DataRequired()])
    date = DateField("Event Date (YY-MM-DD)",format='%Y-%m-%d',validators=[validators.DataRequired(),DateRange(min=date.today(),message = "Please enter a valid date")])
    time = TimeField("Start Time (HH:MM)",format='%H:%M')
    place = StringField("Place", validators=[validators.DataRequired()])
    content = TextAreaField("Content of the Event", validators=[validators.Length(min=10)])
    
