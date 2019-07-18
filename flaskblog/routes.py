from flask import render_template, url_for, flash, redirect, request, abort
#functions responsible with the management of the pages
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
#form created by us 
from flaskblog.models import User, Post
#imports the database fields so we know how to work with it 
from flaskblog import app, db, bcrypt, mail 

from flask_login import login_user, current_user, logout_user, login_required

from flask_mail import Message

from PIL import  Image

#lib used for randomising
import secrets

#lib used for getting paths
import os


"""
app is responsible with the routs and keeps track of the files?
db is the database
bcrypt is an object that has the hashing functions
"""
Title = "SynBlog"

@app.route("/")
@app.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page = 5)
	#used for pagination and order by date desc
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
			flash("User logged in successfully!",'success')
			if not next_page:
				return redirect(url_for('home'))
			else:
				return redirect(url_for(next_page[1:]))
		else:
			flash('Login unsuccessful, check your email and password!','danger')

	return render_template('login.html', title='Login', form = form )



@app.route("/logout")
@login_required
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


@app.route("/post/<int:post_id>")
#post_id is a var that is the id of a post
def post(post_id):
	post = Post.query.get_or_404(post_id)
	#gets post or gives error
	return render_template('post.html', title = post.title, post=post)


@app.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
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


@app.route("/post/<int:post_id>/delete",methods  = ['POST','GET'])
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


@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username = username).first_or_404()

	posts = Post.query\
		.filter_by(author = user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page = page,per_page = 5)
	return render_template('user_post.html',posts=posts, user=user)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password reset request',
	 			  sender='noreply@demo.com', 
	 			  recipients=[user.email])
	msg.body = f"""To reset your password visit: {url_for('reset_token', token =token, _external =True)}
If you did not make this request please ignore it!
	"""
	mail.send(msg)





@app.route("/reset_password",methods  = ['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		flash("User already logged in!",'danger')
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("A reset email was sent!","info")
		return redirect(url_for("login"))

	return render_template('reset_request.html', title = "Reset Password", form = form)

@app.route("/reset_password/<token>",methods  = ['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		flash("User already logged in!",'danger')
		return redirect(url_for('home'))

	user = User.verify_reset_token(token)
	if user is None:
		flash("Invalid or expired token!","warning")
		return redirect(url_for("reset_request"))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		flash( f'Account updated!','success' )
		user.password = hashed_password
		db.session.commit()
		return redirect(url_for('login'))

	return render_template('reset_token.html', title = "Reset Passwprd", form = form)
