from __init__ import db
from datetime import datetime


class Links(db.Model):
    link_id = db.Column(db.String(5), primary_key=True)
    link = db.Column(db.String(1000))
    username = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<link {}>'.format(self.link)


class Treelinks(db.Model):
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