import sys

sys.path.append("../")
from flaskblog import app

sys.path.append("../")
from flaskblog.models import User, Post

from test_manage_users import get_a_user_from_the_db


def test_login_a_user_from_the_db_with_valid_credentials(get_a_user_from_the_db):
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'login',
			data = dict(
				email = user.email,
				password = user.password,
				),
			follow_redirects = True
			)
	assert b"User logged in successfully!" in response.data
	assert response.status_code == 200

def test_login_a_user_from_the_db_with_incorrect_password(get_a_user_from_the_db):
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'login',
			data = dict(
				email = user.email,
				password = user.password+"a",
				),
			follow_redirects = True
			)
	assert b"User logged in successfully!" not in response.data
	assert response.status_code == 200


def test_login_a_user_from_the_db_with_incorect_email(get_a_user_from_the_db):
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'login',
			data = dict(
				email = user.email+"a",
				password = user.password,
				),
			follow_redirects = True
			)
	assert b"User logged in successfully!" not in response.data
	assert response.status_code == 200

def test_login_a_user_from_the_db_with_invalid_email_format(get_a_user_from_the_db):
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'login',
			data = dict(
				email = user.username,
				password = user.password,
				),
			follow_redirects = True
			)
	assert b"User logged in successfully!" not in response.data
	assert response.status_code == 200

def test_login_a_user_with_missing_email_and_password_fields(get_a_user_from_the_db):
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'login',
			data = dict(
				email = "",
				password = "",
				),
			follow_redirects = True
			)
	assert b"User logged in successfully!" not in response.data
	assert response.status_code == 200
