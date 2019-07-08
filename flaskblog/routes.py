from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app

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
    return render_template('home.html',posts=posts, title=Title )


@app.route("/about")
def about():
    return render_template('about.html', title=Title )


@app.route("/register", methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	#checks for valid data for the register
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!','succes')
		return redirect(url_for('home'))
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

