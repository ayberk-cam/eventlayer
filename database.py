import psycopg2
from classes import Student,StudentClub,Event
import datetime
from flask import current_app

class Database:
    def __init__(self,filename):
        self.filename = filename
        self.connection = psycopg2.connect(self.filename)
        with self.connection:
            with self.connection.cursor() as cursor:
                query = """CREATE TABLE IF NOT EXISTS Student (
                                student_id SERIAL PRIMARY KEY,
                                name VARCHAR NOT NULL,
                                surname VARCHAR NOT NULL,
                                department VARCHAR NOT NULL,
                                username VARCHAR UNIQUE NOT NULL,
                                email VARCHAR UNIQUE NOT NULL,
                                crypted_password VARCHAR NOT NULL
                                );
                            CREATE TABLE IF NOT EXISTS Student_Club (
                                studentclub_id SERIAL PRIMARY KEY,
                                name VARCHAR NOT NULL,
                                profession VARCHAR NOT NULL,
                                username VARCHAR UNIQUE NOT NULL,
                                email VARCHAR UNIQUE NOT NULL,
                                crypted_password VARCHAR NOT NULL
                                );
                            CREATE TABLE IF NOT EXISTS Events(
                                event_id SERIAL PRIMARY KEY,
                                studentclub_id INTEGER NOT NULL,
                                club_name VARCHAR NOT NULL,
                                name VARCHAR NOT NULL,
                                date DATE NOT NULL,
                                time TIME NOT NULL,
                                place VARCHAR NOT NULL,
                                content TEXT NOT NULL,
                                FOREIGN KEY(studentclub_id) REFERENCES Student_Club(studentclub_id)
                                );
                            CREATE TABLE IF NOT EXISTS Member(
                                member_id SERIAL PRIMARY KEY,
                                student_id INTEGER NOT NULL,
                                studentclub_id INTEGER NOT NULL,
                                FOREIGN KEY(student_id) REFERENCES Student(student_id),
                                FOREIGN KEY(studentclub_id) REFERENCES Student_Club(studentclub_id)
                                );"""
                cursor.execute(query)
                
    def registerStudent(self,student):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO Student (name, surname, department, username, email, crypted_password) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (student.name, student.surname, student.department, student.username, student.email, student.password) )
                self.connection.commit()
        return

    def registerStudentClub(self,studentclub):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO Student_Club (name, profession, username, email, crypted_password) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(query, (studentclub.club_name, studentclub.club_profession, studentclub.club_username, studentclub.club_email, studentclub.club_password) )
                self.connection.commit()
        return

    def getStudent(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT name, surname, department, username, email, crypted_password FROM Student WHERE username = (%s)"
                cursor.execute(query,(username,))
                a,b,c,d,e,f = cursor.fetchone()
        selectedUser = Student(a,b,c,d,e,f)
        return selectedUser

    def getStudentId(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT student_id FROM Student WHERE username = (%s)",(username,))
                selected_user_id = cursor.fetchone()
        return selected_user_id
    
    def getStudentBool(self,student_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "select exists(select 1 from student where student_id=(%s)))"
                result = cursor.execute(query,(student_id,))
        return result
    
    def getStudentClub(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT name, profession, username, email, crypted_password FROM Student_Club WHERE username = (%s)"
                cursor.execute(query,(username,))
                a,b,c,d,e = cursor.fetchone()
        selectedUser = StudentClub(a,b,c,d,e)
        return selectedUser

    def getClubId(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT studentclub_id FROM Student_Club WHERE username = (%s)",(username,))
                selected_user_id = cursor.fetchone()
        return selected_user_id
    
    def getClubName(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT name FROM Student_Club WHERE username = (%s)",(username,))
                selected_user_name = cursor.fetchone()
        return selected_user_name
   
    def addEvent(self,event):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO Events (studentclub_id, club_name, name, date, time, place, content) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (event.club_id, event.club_name, event.event_name, event.event_date, event.event_time, event.event_place, event.event_content) )
                self.connection.commit()
        return

    def getEvents(self,studentclub_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM Events WHERE studentclub_id = (%s)"
                cursor.execute(query,(studentclub_id,))
                events_ = cursor.fetchall()
        return events_

    def getEvent(self,event_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM Events WHERE event_id = (%s)"
                cursor.execute(query,(event_id,))
                event_ = cursor.fetchone()
        return event_

    def deleteEvent(self,event_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM Events WHERE event_id = (%s)",(event_id,))
                self.connection.commit()
        return
    
    def getStudentClubIdfromEvent(self,event_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT studentclub_id FROM Events WHERE event_id = (%s)",(event_id,))
                selected_user_id = cursor.fetchone()
        return selected_user_id

    def updateEvent(self,event):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "UPDATE Events SET name = %s, date = %s, time = %s, place = %s, content = %s WHERE event_id = (%s)"
                cursor.execute(query,(event.event_name ,event.event_date, event.event_time, event.event_place, event.event_content, event.id))
                self.connection.commit()
        return

    def getAllEvents(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM Events"
                cursor.execute(query)
                events = cursor.fetchall()
        return events

    def beMember(self,member):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO Member (studentclub_id, student_id) VALUES (%s,%s)"
                cursor.execute(query, (member.club_id, member.student_id))
                self.connection.commit()
        return

    def getAllClubs(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM Student_Club"
                cursor.execute(query)
                clubs = cursor.fetchall()
        return clubs
    
    def getStudentClubIdfromMember(self,studentclub_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT student_id FROM Member WHERE studentclub_id = (%s)",(studentclub_id,))
                selected_user_id = cursor.fetchone()
        return selected_user_id

    def getMember(self,studentclub_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT student_id FROM Member WHERE studentclub_id = (%s)",(studentclub_id,))
                selected_user_id = cursor.fetchall()
        return selected_user_id

    def getStudentforMember(self,student_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT name, surname, department,email FROM Student WHERE student_id = (%s)"
                cursor.execute(query,(student_id,))
                member = cursor.fetchall()
        return member