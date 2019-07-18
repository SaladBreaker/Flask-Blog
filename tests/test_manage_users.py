import sys

sys.path.append("../")
from flaskblog import app, db

sys.path.append("../")
from flaskblog.models import User, Post

import pytest
import random
import string

post_dummy_id = 1

def random_string():
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(15))

def give_id_for_testing_post():
	user = User.query.filter_by(email = "test1@gmail.com").first()
	if user == None:
		user = User(
			username = "test1",
			email = "test1@gmail.com",
			password = "test1"
			)
		db.session.add(user)
		db.session.commit()
	
	if user == None:
		assert False, "Error at adding a dummy user for testing"

	posts = user.getPostsIds()
	if len(posts) == 0:
		post = Post(
			title = "test1",
			content = "test1",
			author = user)
		db.session.add(post)
		db.session.commit()

	posts = user.getPostsIds()
	
	if len(posts) == 0:
		assert False, "Error at adding a dummy post for testing"
	return str(posts[0])


@pytest.fixture
def get_a_user_from_the_db():
	give_id_for_testing_post()
	user = User(
		username = "test1",
		email = "test1@gmail.com",
		password = "test1",
		)
	return user

@pytest.fixture
def create_data_for_a_new_user():
	txt = random_string()
	user = User(
		username = txt,
		email = txt + "@gmail.com",
		password = txt,
		)
	return user

def delete_a_given_user_from_the_db(user):
	User.query.filter_by(email = user.email).delete()
