import sys
sys.path.append("../")
from flaskblog import app, db

sys.path.append("../")
from flaskblog.models import User, Post

import pytest
import random
import string


dummy_user = User()

def random_string():
	letters= string.ascii_lowercase
	return ''.join(random.sample(letters,20))


@pytest.fixture
def create_a_random_user():
	string = random_string()
	user = User( username = string, email = string + "@gamil.com", password = string)
	return user

@pytest.fixture
def get_a_user_from_the_database():
	global dummy_user
	return dummy_user

@pytest.fixture
def register_a_random_user(create_a_random_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_a_random_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'/register',
			data = dict(
				username = user.username,
				email = user.email,
				password = user.password,
				confirm_password = user.password
				),
			follow_redirects = True
			)
	assert b"Account created" in response.data
	assert response.status_code == 200
	return user


@pytest.fixture
def login_a_dummy_user_from_the_database(get_a_user_from_the_database):
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_database

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'/login',
			data = dict(
				email = user.email,
				password = user.password,
				),
			follow_redirects = True
			)

	assert b"User logged in successfully!" in response.data
	assert response.status_code == 200
	return user


def test_if_a_random_user_can_register_with_valid_credentials(register_a_random_user):
	global dummy_user
	dummy_user = register_a_random_user
	 

def test_if_a_user_can_login_with_valid_credentials(login_a_dummy_user_from_the_database):
	login_a_dummy_user_from_the_database