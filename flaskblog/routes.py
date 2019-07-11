from flask import render_template, url_for, flash, redirect, request, abort
#functions responsible with the management of the pages
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
#form created by us 
from flaskblog.models import User, Post
#imports the database fields so we know how to work with it 
from flaskblog import app, db, bcrypt

from flask_login import login_user, current_user, logout_user, login_required

from PIL import  Image

#lib used for randomising
import secrets
#lib used for getting paths
import os
#

"""
app is responsible with the routs and keeps track of the files?
db is the database
bcrypt is an object that has the hashing functions
"""
Title = "SynBlog"

@app.route("/")
@app.route("/home")
def home():
	posts = Post.query.all()
	#render_template(calls the html page with the given parameters)
	return render_template('home.html',posts=posts, title=Title)


@app.route("/about")
def about():
    return render_template('about.html', title=Title)


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
		flash( f'Account created for {form.username.data}. You can now login!','success' )
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
			flash('Login unsuccessful, check your email and password!','danger')
	return render_template('login.html', title='Login', form = form )



@app.route("/logout")
def logout():
	#function that log outs user
	logout_user()
	return redirect(url_for('home'))




def save_picture(form_picture):
	#use random name to the photo so there are no duplicates
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	#gets the file extension and sets the name <random>.png or jpg
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	#creates the path of the file in the current app dir
	
	output_size = (125,125)
	i =Image.open(form_picture)
	i.thumbnail(output_size)
	#resizing the iamge

	i.save(picture_path)
	return picture_fn

@app.route("/account", methods = ['GET', 'POST'])
#login required route set in __init__.py
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_name = save_picture(form.picture.data)
			current_user.image_file = picture_name
		#validate on submit check for fct with validate_*
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		#Updates the user info
		flash('Your account info has been updated!','success')
		return redirect(url_for("account"))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static' , filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file = image_file, form =form)



@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash("Good post!","success")
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', form=form, legend ="New Post")


@app.route("/post/<post_id>")
#post_id is a var that is the id of a post
def post(post_id):
	post = Post.query.get_or_404(post_id)
	#gets post or gives error
	return render_template('post.html', title = post.title, post=post)


@app.route("/post/<post_id>/update", methods = ['GET', 'POST'])
@login_required
#post_id is a var that is the id of a post
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		#403 - forbitten route
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash("Post Updated!", 'success')
		return redirect(url_for('post',post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title 
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form, legend ="Update Post")


@app.route("/post/<post_id>/delete",methods  = ['POST'])
@login_required
#post_id is a var that is the id of a post
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		#403 - forbitten route
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Post Deleted!", 'success')
	return redirect(url_for('home'))
