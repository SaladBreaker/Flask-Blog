import sys

sys.path.append("../")
from flaskblog import app

from test_manage_users import give_id_for_testing_post

""" Restricted pages"""
def test_unlogged_user_redirects_to_login_when_accesing_account():	
	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'/account',
			follow_redirects = True
			)
	assert b"Please log in to access this page." in response.data 

def test_unlogged_user_redirects_to_login_when_accesing_logout():	
	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'/logout',
			follow_redirects = True
			)
	assert b"Please log in to access this page." in response.data 

def test_unlogged_user_redirects_to_login_when_accesing_post_new():	
	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'/post/new',
			follow_redirects = True
			)
	assert b"Please log in to access this page." in response.data 

def test_unlogged_user_redirects_to_login_when_accesing_post_id_update():	
	id = give_id_for_testing_post()
	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'/post/' + id +'/update',
			follow_redirects = True
			)
	assert b"Please log in to access this page." in response.data 

def test_unlogged_user_redirects_to_login_when_accesing_post_id_delete():	
	id = give_id_for_testing_post()

	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'/post/' + id +'/delete',
			follow_redirects = True
			)
	assert b"Please log in to access this page." in response.data 



""" Accesible pages"""
def test_unlogged_user_can_access_home_page():	
	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'home',
			follow_redirects = True
			)
	assert response.status_code == 200

def test_unlogged_user_can_access_post_id():	
	id = give_id_for_testing_post()

	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'post/' + id,
			follow_redirects = True
			)
	assert response.status_code == 200

def test_unlogged_user_can_access_user_posts():	
	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.get(
			'user/test1',
			follow_redirects = True
			)
	assert response.status_code == 200

