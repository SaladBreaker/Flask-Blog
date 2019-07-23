from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

"""
user SynBlogBot@gmail.com
pass SynBLog.default

"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s -- %(name)s] %(message)s")
file_handler = logging.FileHandler("../logs/init.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


app = Flask(__name__)
logger.info(f"App started successfully!")

app.config["SECRET_KEY"] = "qSrbDdD5vTM4XEiG"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "SynBlogBot@gmail.com"
app.config["MAIL_PASSWORD"] = "SynBlog.default"
logger.info(f"App configured successfully!")

db = SQLAlchemy(app)
logger.info(f"Database loaded successfully!")

bcrypt = Bcrypt(app)
logger.info(f"Encrypting key created successfully!")

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
logger.info(f"Login manager created successfully!")


mail = Mail(app)
logger.info(f"Mail sender created successfully!")

from flaskblog import routes
