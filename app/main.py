import uuid
import logging

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from utils import LoginForm, mydb, tree
from parse_multilink import create_multilink
from config import Config
from shortlink import shortlink_blueprint
from statistics import statistic_blueprint

application = Flask(__name__)
application.config.from_object(Config)
application.register_blueprint(shortlink_blueprint)
application.register_blueprint(statistic_blueprint)

logging.basicConfig(encoding='utf-8', level=logging.INFO)

db = SQLAlchemy(application)


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


@application.route('/')
def hello():
    return render_template('index.html')


@application.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')


@application.route('/registration', methods=['POST', 'GET'])
def registration():
    form = LoginForm()
    if form.validate_on_submit():
        logging.info('Login requested for user {}, remember_me={}, password {}'.format(
            form.username.data, form.remember_me.data, form.password.data))
        return redirect('/')
    return render_template('registration.html', title='Sign In', form=form)


@application.route('/statistic')
def statistic():
    return render_template('stat.html')


@application.route('/multilink')
def multilink():
    return render_template('multilink.html')


def cut(link_id):
    link = Links.query.filter_by(link_id=link_id).first()
    if link is None:
        return '<h3>Нет такой короткой ссылки</h3>'
    logging.info('link - {}'.format(link.link))
    return redirect(link.link, code=302)


@application.route("/<link_id>")
def multiple(link_id):
    click = Clicks(link=link_id)
    db.session.add(click)
    db.session.commit()

    if len(link_id) == 4:
        return cut(link_id)
    else:
        return tree(link_id)


@application.route('/your_short_link', methods=['POST', 'GET'])
def your_short_link():
    link = request.form['link']
    hash = uuid.uuid4().hex[:4]
    username = 'site'

    link = Links(link_id=hash, link=link, username=username)
    db.session.add(link)
    db.session.commit()

    return render_template('shortlink.html', forward_message=f'http://cutlinks.ru/{hash}')


@application.route('/your_tree_link', methods=['POST', 'GET'])
def your_tree_link():
    hash = create_multilink(request, mydb)
    return render_template('multilink.html', forward_message=f'{hash}')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
