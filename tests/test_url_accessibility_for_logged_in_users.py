import sys

sys.path.append("../")
from flaskblog import app

from test_manage_users import get_a_user_from_the_db, give_id_for_testing_post


def test_logged_user_can_access_urlfor_account(get_a_user_from_the_db):	

	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'/account',
			follow_redirects = True
			)
	assert b"Please log in to access this page."  not in response.data 


def test_logged_user_can_access_urlfor_logout(get_a_user_from_the_db):	

	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'/logout',
			follow_redirects = True
			)
	assert b"Please log in to access this page."  not in response.data 

def test_logged_user_can_access_urlfor_post_delete(get_a_user_from_the_db):	
	id = give_id_for_testing_post()
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'/post/' + id +'/delete',
			follow_redirects = True
			)
	assert b"Please log in to access this page."  not in response.data 

def test_logged_user_can_access_urlfor_post_update(get_a_user_from_the_db):	
	id = give_id_for_testing_post()
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'/post/' + id +'/update',
			follow_redirects = True
			)
	assert b"Please log in to access this page."  not in response.data 

def test_logged_user_can_access_urlfor_post_new(get_a_user_from_the_db):	
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'/post/new',
			follow_redirects = True
			)
	assert b"Please log in to access this page."  not in response.data 



def test_logged_user_can_access_home_page(get_a_user_from_the_db):	
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'home',
			follow_redirects = True
			)
	assert response.status_code == 200

def test_logged_user_can_access_post_id(get_a_user_from_the_db):	
	id = give_id_for_testing_post()

	user = get_a_user_from_the_db
	app.config['WTF_CSRF_ENABLED'] = False
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
		
		response = tester.get(
			'post/' + id,
			follow_redirects = True
			)
	assert response.status_code == 200

def test_logged_user_can_access_user_posts(get_a_user_from_the_db):	
	app.config['WTF_CSRF_ENABLED'] = False

	user = get_a_user_from_the_db
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

		response = tester.get(
			'user/test1',
			follow_redirects = True
			)
	assert response.status_code == 200