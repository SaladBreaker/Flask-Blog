from flask import render_template, url_for, flash, redirect
#functions responsible with the management of the pages
from flaskblog.forms import RegistrationForm, LoginForm
#form created by us 
from flaskblog.models import User, Post
#imports the database fields so we know how to work with it 
from flaskblog import app, db, bcrypt
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
	form = LoginForm()
	#checks for valid data for the login
	if form.validate_on_submit():
			if form.email.data == 'a@gmail.com' and form.password.data == '12345':
				flash(f'Login succesful for {form.email.data}!','succes')
				return redirect(url_for('home'))
			else:
				flash('Login unsuccesful!','danger')
				return redirect(url_for('home'))
	return render_template('login.html', title='Login', form = form )

