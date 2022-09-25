from flask import session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """creates a user"""
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key = True, unique=True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50),nullable = False,unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))

    feedback = db.relationship('Feedback', backref = "user", cascade = "all,delete-orphan")


    def login(self,pwd):
        """checks for user/pwd combo in db, sets the session, and returns bool"""
    
        if Bcrypt().check_password_hash(self.password, pwd):
            session["username"] = self.username
            return True   
        return False

    @classmethod
    def register(cls,userN,pwd,first,last,email):
        hashed = Bcrypt().generate_password_hash(pwd).decode("utf-8")
        return cls(username=userN, password=hashed, first_name=first, last_name=last, email=email)


class Feedback(db.Model):
    """table for feedback"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))



    