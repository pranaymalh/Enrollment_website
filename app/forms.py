from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from app.models import User

class LoginForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
	remember_me=BooleanField("Remember Me")
	submit=SubmitField("Login")

	

class RegisterForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
	password_confirm=PasswordField("Password Confirm",validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
	first_name=StringField("First Name",validators=[DataRequired(),Length(min=2,max=55)])
	last_name=StringField("Last Name",validators=[DataRequired(),Length(min=2,max=55)])
	submit=SubmitField("Register")