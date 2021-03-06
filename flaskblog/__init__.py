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
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s -- %(name)s] %(message)s")
"""if os.getcwd().split("\\")[-1] != "WebAPP":
    file_handler = logging.FileHandler("../logs/events.log")
else:
    file_handler = logging.FileHandler("logs/events.log")"""
file_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

try:
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
except:
    logger.fatal(f"App could not start!!!")
