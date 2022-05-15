class Config(object):
    database = 'u1650045_default',
    host = "cutlinks.ru",
    user = "u1650045_default",
    password = "mqGIBF31HU1x8zxo"

    # не работает почему то
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}:/{database}'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://u1650045_default:mqGIBF31HU1x8zxo@cutlinks.ru/u1650045_default'
    SECRET_KEY = 'some-easy-key'