from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Links(db.Model):
    link_id = db.Column(db.String(5), primary_key=True)
    link = db.Column(db.String(1000))
    username = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<link {}>'.format(self.link)


class TreeLinks(db.Model):
    link_id = db.Column(db.String(6), primary_key=True)
    link = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    username = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<link {}>'.format(self.link)


class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<link {}>'.format(self.link)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
