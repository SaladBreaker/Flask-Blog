import sys
sys.path.append("../")
from flaskblog import app


def test_login():
	# csrf_token

	app.config['WTF_CSRF_ENABLED'] = False
	with app.test_request_context():
		tester = app.test_client()
		response = tester.post(
			'/login',
			data = dict(
				email = "dummy@gmail.com",
				password = "dummy"
				),
			follow_redirects = True)
	assert b"User logged in successfully!" in response.data




"""def test_login():
	TESTEMAIL = "dummy@gmail.com"
	TESTPASS = "dummy"
	form = LoginForm(
		formdata = None, 
		email = "dummy@gmail.com",
		password = "dummy"
		)
	with app.test_request_context():
		with app.test_client() as c:
			with c.session_transaction() as sess:
				sess['email'] = TESTEMAIL
				sess['password'] = TESTPASS
				response = c.post(
					'/login',
					data = form.data,
					follow_redirects =True
					)
	assert "User logged in successfully!" in response.data"""