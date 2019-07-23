from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    PostForm,
    RequestResetForm,
    ResetPasswordForm,
)

from flaskblog.models import User, Post

from flaskblog import app, db, bcrypt, mail

from flask_login import login_user, current_user, logout_user

from flask_mail import Message

from PIL import Image

import secrets

import os

import functools

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s -- %(name)s] %(message)s")
file_handler = logging.FileHandler("../logs/routes.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

Title = "SynBlog"


def required_login(func):
    @functools.wraps(func)
    def wrapper(post_id=-1):
        if not current_user.is_authenticated:
            abort(403)

        if post_id != -1:
            return func(post_id)
        else:
            return func()

    return wrapper


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    if current_user.is_authenticated:
        logger.debug(
            f"Home page accessed successfully. User: {current_user.email}. IP: {request.remote_addr}"
        )
    else:
        logger.debug(
            f"Home page accessed successfully. User: Unknown. IP: {request.remote_addr}"
        )

    return render_template("home.html", posts=posts, title=Title)


@app.route("/about")
def about():
    logger.debug(
        f"About page accessed successfully. User: {current_user.email}. IP: {request.remote_addr}"
    )
    return render_template("about.html", title=Title)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        logger.debug(
            f"Already logged in user tried to register. User: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("User already logged in!", "danger")

        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        flash(
            f"Account created for {form.username.data}. You can now login!", "success"
        )

        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )

        try:
            db.session.add(user)
            db.session.commit()

        except Exception as e:
            logger.warning(
                f"Could not save user to database. User: {user.email}. IP: {request.remote_addr}"
            )
            flash("Unexpected error at registering. Please try again!", "danger")

            return redirect(url_for("register"))

        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("User already logged in!", "danger")
        logger.debug(
            f"Already logged in user tried to login. User {current_user.email}. IP: {request.remote_addr}"
        )

        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("User logged in successfully!", "success")
            logger.debug(
                f"User login successfully. User {current_user.email}. IP: {request.remote_addr}"
            )

            if not next_page:
                return redirect(url_for("home"))
            else:
                return redirect(url_for(next_page[1:]))

        else:
            logger.debug(
                f"User login unsuccessfully invalid credentials!. IP: {request.remote_addr}"
            )
            flash("Login unsuccessful, check your email and password!", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@required_login
def logout():
    logout_user()
    logger.debug(f"User log out successfully! IP: {request.remote_addr}")

    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    logger.debug(
        f"Photo saved successfully for: {current_user.email}. IP: {request.remote_addr}"
    )

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@required_login
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name

        try:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
        except Exception as e:
            logger.warning(
                f"CAn not update info for: {current_user.email}. IP: {request.remote_addr}"
            )
            flash("Unexpected error at updating info. Please try again!", "danger")
            return redirect(url_for("account"))

        logger.debug(
            f"User updated successfully: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("Your account info has been updated!", "success")
        return redirect(url_for("account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/post/new", methods=["GET", "POST"])
@required_login
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        try:
            db.session.add(post)
            db.session.commit()

        except Exception as e:
            logger.warning(
                f"Could not create post: { form.title.data }, user: {current_user.email}. IP: {request.remote_addr}"
            )
            flash("Unexpected error at creating post. Please try again!", "danger")
            return redirect(url_for("new_post"))

        logger.debug(
            f"User posted successfully: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("Good post!", "success")
        return redirect(url_for("home"))

    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/post/<int:post_id>")
def post(post_id):

    post = Post.query.get_or_404(post_id)

    if current_user.is_authenticated:
        logger.debug(
            f"User accessed post successfully: {current_user.email}. IP: {request.remote_addr}"
        )
    else:
        logger.debug(
            f"User accessed post successfully: Unknown. IP: {request.remote_addr}"
        )

    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@required_login
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        logger.debug(
            f"User: {current_user.email} without accessed tried to access post:{post.getId()}. IP: {request.remote_addr}"
        )
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        try:
            db.session.commit()

        except Exception as e:
            logger.warning(
                f"Could not update post: {current_user.email} post id:{post.getId()}. IP: {request.remote_addr}"
            )
            flash("Unexpected error at updating post. Please try again!", "danger")
            return redirect(url_for("update_post", post_id))

        logger.debug(
            f"Post updated successfully: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("Post Updated!", "success")
        return redirect(url_for("post", post_id=post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/post/<int:post_id>/delete", methods=["POST", "GET"])
@required_login
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    logger.debug(
        f"User tries to delete post: {current_user.email} post id:{post.getId()}. IP: {request.remote_addr}"
    )

    if post.author != current_user:
        abort(403)

    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        logger.warning(
            f"Could not delete post. Post id:{post.getId()}, user: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("Unexpected error at deleting post. Please try again!", "danger")
        return redirect(url_for("home"))

    flash("Post Deleted!", "success")
    logger.debug(
        f"Post deleted successfully. User: {current_user.email}. IP: {request.remote_addr}"
    )
    return redirect(url_for("home"))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )

    if current_user.is_authenticated:
        logger.debug(
            f"User's profile successfully accessed. User: {current_user.email}, Accessed user: { user.email }. IP: {request.remote_addr}"
        )
    else:
        logger.debug(
            f"User's profile successfully accessed. User: Unknown, Accessed user: { user.email }. IP: {request.remote_addr}"
        )

    return render_template("user_post.html", posts=posts, user=user)


def send_reset_email(user):
    try:
        token = user.get_reset_token()
        msg = Message(
            "Password reset request", sender="noreply@demo.com", recipients=[user.email]
        )

        msg.body = f"""To reset your password visit: {url_for('reset_token', token =token, _external =True)}
    If you did not make this request please ignore it!
        """
        mail.send(msg)
    except Exception as e:
        logger.warning(
            f"Could not send recovery email to: { user.mail }. IP: {request.remote_addr}"
        )


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():

    if current_user.is_authenticated:
        logger.debug(
            f"Logged in user tried to reset password. User: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("User already logged in!", "danger")
        return redirect(url_for("home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        try:
            send_reset_email(user)

        except Exception as e:
            flash("Unexpected error at sending mail. Please try again!", "danger")
            logger.warning(
                f"Mail could not be sent. User: {user.email}. IP: {request.remote_addr}"
            )
            return redirect(url_for("register"))

        logger.debug(
            f"Recovery mail sent. Email: {user.email} . IP: {request.remote_addr}"
        )
        flash("A reset email was sent!", "info")

        return redirect(url_for("login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):

    if current_user.is_authenticated:
        logger.debug(
            f"Logged user tried to reset password: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("User already logged in!", "danger")
        return redirect(url_for("home"))

    user = User.verify_reset_token(token)
    if user is None:
        logger.debug(
            f"User gave an expired token: {current_user.email}. IP: {request.remote_addr}"
        )
        flash("Invalid or expired token!", "warning")
        return redirect(url_for("reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        flash(f"Account updated!", "success")

        try:
            user.password = hashed_password
            db.session.commit()

        except Exception as e:
            flash("Unexpected error at validating token. Please try again!", "danger")
            logger.warning(
                f"Token could not be validated. User: {user.email}. IP: {request.remote_addr}"
            )
            return redirect(url_for("home"))

        logger.debug(
            f"Password reset successfully for: {current_user.email}. IP: {request.remote_addr}"
        )
        return redirect(url_for("login"))

    return render_template("reset_token.html", title="Reset Password", form=form)
