import sys
import os

if os.getcwd().split("\\")[-1] != "WebAPP":
    sys.path.append("../")
    from flaskblog import app, db

    sys.path.append("../")
    from flaskblog.models import User, Post
else:
    from flaskblog import app, db
    from flaskblog.models import User, Post

import pytest
import random
import string


def random_string():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(15))


@pytest.fixture
def post():
    user = User.query.filter_by(email="test1@gmail.com").first()

    if user == None:
        user = User(username="test1", email="test1@gmail.com", password="test1")
        db.session.add(user)
        db.session.commit()

    assert user != None, "Error at adding a dummy user for testing"

    posts = user.getPosts()
    if len(posts) == 0:
        post = Post(title="test1", content="test1", author=user)
        db.session.add(post)
        db.session.commit()
        return post

    assert posts != None, "Error at adding a dummy post for testing"

    return posts[0]


@pytest.fixture
def configed_app():
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture
def client(configed_app):
    return configed_app.test_client()


@pytest.fixture
def user():
    return User(username="test1", email="test1@gmail.com", password="test1")


@pytest.fixture
def new_user():
    txt = random_string()
    return User(username=txt, email=txt + "@gmail.com", password=txt)


@pytest.fixture
def login(client, user):
    response = client.post(
        "/login",
        data=dict(email=user.email, password=user.password),
        follow_redirects=True,
    )

    assert response.status_code == 200, "Login fixture failed"

    return response


@pytest.fixture
def logout(user, client):
    response = client.get("/logout", follow_redirects=False)
    assert (
        response.status_code == 302 or response.status_code == 403
    ), "Logout fixture failed"
    return response


@pytest.fixture
def register(client, new_user):
    user = new_user
    response = client.post(
        "register",
        data=dict(
            username=user.username,
            email=user.email,
            password=user.password,
            confirm_password="",
        ),
        follow_redirects=False,
    )

    assert response.status_code == 200, "Register fixture failed"


def delete_user(user=None):
    if user != None:
        User.query.filter_by(email=user.email).delete()
    else:
        assert user != none, "Trying to delete None object instead of user obj"


def get_posts_from_db(user):
    assert db != None, "Inexistent db"
    return Post.query.filter_by(author=user).all()
