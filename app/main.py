import uuid
import logging

from flask import redirect, render_template, request

from utils import LoginForm, mydb, tree
from parse_multilink import create_multilink

from __init__ import db, create_app
from models import Links, Clicks, Treelinks
application = create_app()

logging.basicConfig(encoding='utf-8', level=logging.INFO)


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
    logging.info('click - {}'.format(link_id))
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
