from main import create_app
from main import db

if __name__ == "__main__":
    app = create_app()
    app.config["db"] = db
    app.config["SECRET_KEY"] = "eventlayer"
    app.run()