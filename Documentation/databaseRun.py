import sys
sys.path.append('../')

from flaskblog import db
from flaskblog.models import User, Post

db.create_all()

"""
Useful functions


Declare and init the db:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

Creates the db with all the fields:
A field is declared by using a class with the inheritance Name_Class(db.Model)
db.create_all()

Print:
print(User.query.all())

Adding:
db.session.add(guest)
db.session.commit()

Searching:
User.query.filter_by(username='admin').first()	
								      .all()
Post.query.with_parent(py).filter(Post.title != 'Snakes').all()


"""
