import sys
sys.path.append("../")
from flaskblog import app
sys.path.append("../flaskblog")
from forms import LoginForm


def test_login(app):
	# csrf_token
	with app.test_request_context('/login'):
		form_a = LoginForm(
			formdata=None, 
			email = "dummy@gmail.com",
			password = "dummy", 
			submit="Login"
			)
		tester = app.test_client()
		tester.post(
			'/login',
			data = dict(form_a.data),
			content_type='multipart/form-data',
			follow_redirects = True)
	assert False