import sys

sys.path.append("../")
from flaskblog import app, db

sys.path.append("../")
from flaskblog.models import User, Post


from test_manage_users import create_data_for_a_new_user, delete_a_given_user_from_the_db


def test_register_a_random_user_with_correct_credentials(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
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
	delete_a_given_user_from_the_db(user)

def test_register_a_random_user_with_missing_confirm_password(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username = user.username,
				email = user.email,
				password = user.password,
				confirm_password = ""
				),
			follow_redirects = True
			)
	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)

def test_register_a_random_user_with_missing_password(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username = user.username,
				email = user.email,
				password = "",
				confirm_password = user.password
				),
			follow_redirects = True
			)
	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)

def test_register_a_random_user_with_missing_email(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username = user.username,
				email = "",
				password = user.password,
				confirm_password = user.password
				),
			follow_redirects = True
			)
	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)
	
def test_register_a_random_user_with_missing_name(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username = "",
				email = user.email,
				password = user.password,
				confirm_password = user.password
				),
			follow_redirects = True
			)
	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)
	
def test_register_a_random_user_with_name_bigger_than_60(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username =  ''.join("a" for i in range(60)) ,
				email = user.email,
				password = user.password,
				confirm_password = user.password
				),
			follow_redirects = True
			)

	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)

def test_register_a_random_user_with_incorrect_email_format(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username =  user.username,
				email = "IdontWantIT!!!",
				password = user.password,
				confirm_password = user.password
				),
			follow_redirects = True
			)

	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)

def test_register_a_random_user_with_password_and_confirm_password_not_matching(create_data_for_a_new_user):
	app.config['WTF_CSRF_ENABLED'] = False

	user = create_data_for_a_new_user

	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'register',
			data = dict(
				username =  user.username,
				email = user.email,
				password = user.password,
				confirm_password = user.password + "a"
				),
			follow_redirects = True
			)

	assert b"Account created" not in response.data
	assert response.status_code == 200
	delete_a_given_user_from_the_db(user)
