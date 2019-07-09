from flaskblog import db, login_manager 
from datetime import datetime 

""" 
Models are used to create the database columns 
(db.Model) paramether adds the given class to the database

login manager:

"""

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(40), unique=True, nullable = False)
	email = db.Column(db.String(140), unique=True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default="default.jpg")
	password = db.Column(db.String(60), nullable = False)
	posts = db.relationship('Post', backref = 'author', lazy = True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)

	def __repr__(self):
		return f"User('{self.title}','{self.date_posted}')"