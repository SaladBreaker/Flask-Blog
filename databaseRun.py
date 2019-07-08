from flaskblog import db
from flaskblog.models import User, Post

print(User.query.all())