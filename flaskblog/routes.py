from flask import render_template, url_for, flash, redirect, request
#functions responsible with the management of the pages
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
#form created by us 
from flaskblog.models import User, Post
#imports the database fields so we know how to work with it 
from flaskblog import app, db, bcrypt

from flask_login import login_user, current_user, logout_user, login_required

"""
app is responsible with the routs and keeps track of the files?
db is the database
bcrypt is an object that has the hashing functions
"""
Title = "Nice Title"

posts = [
	{
		'author': "Jhon",
		'title': "title1",
		'content': "Nice post",
		'date_posted': "April 20,2019"
	},
	{
		'author': 'Jhon the 2',
		'title': 'title2',
		'content': "Nice post2",
		'date_posted': "April 22,2019"
	}

]

@app.route("/")
@app.route("/home")
def home():
	#render_template(calls the html page with the given parameters)
    return render_template('home.html',posts=posts, title=Title )


@app.route("/about")
def about():
    return render_template('about.html', title=Title )


@app.route("/register", methods = ['GET', 'POST'])
#GET is used to give parameters via the path after '?' but does not change them ex: local/username=Vlad
#POST is the same but changes the actual content ex: local/8080
def register():
	#additional checking 
	if current_user.is_authenticated:
		flash("User already logged in!",'danger')
		return redirect(url_for('home'))


	form = RegistrationForm()
	#checks for valid data for the register
	if form.validate_on_submit():
		#apparently validate_on_submit() allow you to create custom validators (check forms.py) 
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		#.decode('utf-8') is for transforming the binary string in a normal string
		flash( f'Account created for {form.username.data}. You can now login!','succes' )
		#add the new user to the db with hashed password
		user = User( username = form.username.data, email = form.email.data, password = hashed_password )
		db.session.add(user)
		db.session.commit()
		#url_for() returns the html page with the given name
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form = form )


@app.route("/login",methods = ['GET', 'POST'])
def login():
	#additional checking 
	if current_user.is_authenticated:
		flash("User already logged in!",'danger')
		return redirect(url_for('home'))


	form = LoginForm()
	#checks for valid data for the login
	if form.validate_on_submit():
		user  = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			#gets the next arg if exists /login?user$next=account
			next_page = request.args.get('next')
			if not next_page:
				return redirect(url_for('home'))
			else:
				return redirect(url_for(next_page[1:]))
		else:
			flash('Login unsuccesful, check your email and password!','danger')
	return render_template('login.html', title='Login', form = form )



@app.route("/logout")
def logout():
	#function that log outs user
	logout_user()
	return redirect(url_for('home'))

@app.route("/account", methods = ['GET', 'POST'])
#login required route set in __init__.py
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		#validate on submit check for fct with validate_*
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		#Updates the user info
		flash('Your account info has beem updated!','succes')
		return redirect(url_for("account"))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static' , filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file = image_file, form =form)