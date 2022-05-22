from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


application = Flask(__name__)
application.config.from_object(Config)

db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
login.login_view = 'login'

from app import routes, models
from app.shortlink import shortlink_blueprint
from app.statistics import statistic_blueprint

application.register_blueprint(shortlink_blueprint)
application.register_blueprint(statistic_blueprint)
