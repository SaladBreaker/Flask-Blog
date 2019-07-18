from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

"""
user SynBlogBot@gmail.com
pass SynBLog.default

"""


app = Flask(__name__)

app.config['SECRET_KEY'] = "qSrbDdD5vTM4XEiG"
#set current location of the db in the current dir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#sets the route for the @login_required and some cathegory


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'SynBlogBot@gmail.com'
app.config['MAIL_PASSWORD'] = 'SynBlog.default'

mail = Mail(app)


from flaskblog import routes