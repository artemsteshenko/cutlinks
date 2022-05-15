from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

from shortlink import shortlink_blueprint
from statistics import statistic_blueprint

db = SQLAlchemy()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)
    application.register_blueprint(shortlink_blueprint)
    application.register_blueprint(statistic_blueprint)
    db.init_app(application)
    return application