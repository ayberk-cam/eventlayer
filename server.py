from flask import Flask
import os
import views
from database import Database


POSTGRESQL_URI = os.environ.get('DATABASE_URL')
db = Database(POSTGRESQL_URI)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/register", view_func=views.register_page)
    app.add_url_rule("/studentregister", view_func=views.studentregister_page, methods=["GET", "POST"])
    app.add_url_rule("/clubregister", view_func=views.clubregister_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page)
    app.add_url_rule("/studentlogin", view_func=views.studentlogin_page, methods=["GET", "POST"])
    app.add_url_rule("/clublogin", view_func=views.clublogin_page, methods=["GET", "POST"])
    app.add_url_rule("/studentlistevents", view_func=views.studentlistevents_page)
    app.add_url_rule("/clublistevents", view_func=views.clubmyevents_page)
    app.add_url_rule("/clubmembers", view_func=views.clubmembers_page)
    app.add_url_rule("/clubaddevent", view_func=views.clubaddevent_page, methods=["GET", "POST"])
    app.add_url_rule("/clubevent/<string:id>", view_func=views.clubevent_page)
    app.add_url_rule("/delete/<string:id>", view_func=views.clubdelete_page)
    app.add_url_rule("/update/<string:id>", view_func=views.clubupdate_page, methods=["GET", "POST"])
    app.add_url_rule("/studentclubs", view_func=views.student_clubs_page)
    app.add_url_rule("/member/<string:id>", view_func=views.member_page)
    app.add_url_rule("/logout", view_func=views.logout_page)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.config["db"] = db
    app.config["SECRET_KEY"] = "eventlayer"
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)