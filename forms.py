from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length

class Signup(FlaskForm):
    """form for logging in"""
    
    first_name = StringField("First Name:", validators =[InputRequired(), Length(max = 30)])
    last_name = StringField("Last Name:", validators =[InputRequired(), Length(max = 30)])
    email = EmailField("User Email:", validators =[InputRequired(), Length(max = 50)])
    username =  StringField("Username:", validators =[InputRequired(), Length(max = 20)])
    password = PasswordField("Password:", validators =[InputRequired()])

class Login(FlaskForm):
    username =  StringField("Username:", validators =[InputRequired(), Length(max = 20)])
    password = PasswordField("Password:", validators =[InputRequired()])

class SubmitFeedBack(FlaskForm):
    content = StringField("Add Text Here: ", validators = [InputRequired()])
