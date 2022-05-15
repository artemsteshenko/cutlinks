from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)
    db.init_app(application)
    return application