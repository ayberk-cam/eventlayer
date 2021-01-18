class Student:
    def __init__(self,name,surname,department,username,email,password):
        self.name = name
        self.surname = surname
        self.department = department
        self.username = username
        self.email = email
        self.password = password

class StudentClub:
    def __init__(self,club_name,club_profession,club_username,club_email,club_password):
        self.club_name = club_name
        self.club_profession = club_profession
        self.club_username = club_username
        self.club_email = club_email
        self.club_password = club_password

class Event:
    def __init__(self,id,club_id,club_name,event_name,event_date,event_time,event_place,event_content):
        self.id = id
        self.club_id = club_id
        self.club_name = club_name
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.event_place = event_place
        self.event_content = event_content

class Member:
    def __init__(self,student_id,club_id):
        self.student_id = student_id
        self.club_id = club_id

