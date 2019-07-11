from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
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


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])
	submit = SubmitField ('Update')

	#add this kind of functions to advance validate input
	def validate_username(self, username):
		if current_user.username != username.data and Email():
			user = User.query.filter_by(username = username.data).first() 
			if user:
				raise ValidationError("Username already registered.")

	def validate_email(self, email):
		if current_user.email != email.data:
			user = User.query.filter_by(email = email.data).first() 
			if user:
				raise ValidationError("Email already registered.")



class PostForm(FlaskForm):
	title = StringField('Title', validators = [DataRequired()])
	content = TextAreaField('Content', validators = [DataRequired()])
	submit = SubmitField('Post!')
