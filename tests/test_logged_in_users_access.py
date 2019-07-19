
from fixtures import user, client, configed_app, login, logout, post

from flask_login import current_user, user_logged_in

def test_logged_user_can_access_account(user,client,configed_app):	
	with configed_app.test_request_context():
		print(user.is_anonymous)
		response = login
		print(user.is_anonymous)
		response = client.get(
			'/account',
			follow_redirects = False
			)
		user_logged_in
	assert b"Please log dsain tso access this page."   in response.data 


"""
def test_logged_user_can_access_logout(user,client,configed_app,login,logout):	
	with configed_app.test_request_context():
		response = login
		response = logout
	assert response.status_code == 302


def test_logged_user_can_access_post_delete(user,client,configed_app,login,post):	
	with configed_app.test_request_context():
		id = str(post.getId())
		logout

		#response = login
		print(user.is_authenticated)
		user.logout
		response = client.get(
			'/post/' + id +'/delete',
			follow_redirects = False)

	assert response.status_code == 403


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
	"""