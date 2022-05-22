import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # database = 'u1650045_default',
    # host = "cutlinks.ru",
    # user = "u1650045_default",
    # password = "mqGIBF31HU1x8zxo",
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-easy-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://u1650045_default:mqGIBF31HU1x8zxo@cutlinks.ru/u1650045_default'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # не работает почему то
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}:/{database}'
