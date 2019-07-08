from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
#parameters gotten from the html forum
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password',validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField ('Sign up')

	#add this kind of functions to advance validate input
	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first() 
		if user:
			raise ValidationError("Username already registered.")

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first() 
		if user:
			raise ValidationError("Email already registered.")

class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password',validators = [DataRequired() ])
	remember = BooleanField('Remember Me')
	submit = SubmitField ('Login')