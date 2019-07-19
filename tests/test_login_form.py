from fixtures import configed_app,user,client


def test_login_succesful_for_valid_credentials(configed_app,user,client):
	with configed_app.test_request_context():
		response = client.post(
			'login',
			data = dict(
				email = user.email,
				password = user.password,
				),
			follow_redirects = False
			)
	assert response.status_code == 302

def test_login_unsuccesful_for_incorrect_password(configed_app,user,client):
	with configed_app.test_request_context():
		response = client.post(
			'login',
			data = dict(
				email = user.email,
				password = user.password+"a",
				),
			follow_redirects = False
			)
	assert response.status_code == 200

def test_login_unsuccesful_for_incorrect_email(configed_app,user,client):
	with configed_app.test_request_context():
		response = client.post(
			'login',
			data = dict(
				email = user.email+"a",
				password = user.password,
				),
			follow_redirects = False
			)
	assert response.status_code == 200

def test_login_unsuccesful_for_incorrect_email_format(configed_app,user,client):
	with configed_app.test_request_context():
		response = client.post(
			'login',
			data = dict(
				email = user.username,
				password = user.password,
				),
			follow_redirects = False
			)
	assert response.status_code == 200

def test_login_unsuccesful_for_missing_fields(configed_app,user,client):
	with configed_app.test_request_context():
		response = client.post(
			'login',
			data = dict(
				email = "",
				password = "",
				),
			follow_redirects = False
			)
	assert response.status_code == 200
