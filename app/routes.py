import uuid
import logging
from flask_login import current_user, login_user, logout_user
from flask import redirect, render_template, request, flash

from app import db, application
from app.models import Links, Clicks, Users
from app.utils import LoginForm, tree, create_multilink, RegistrationForm, cut


logging.basicConfig(encoding='utf-8', level=logging.INFO)


@application.route('/')
def hello():
    return render_template('index.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@application.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@application.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')


@application.route('/statistic')
def statistic():
    return render_template('stat.html')


@application.route('/multilink')
def multilink():
    return render_template('multilink.html')


@application.route("/<link_id>")
def multiple(link_id):
    click = Clicks(link=link_id)
    db.session.add(click)
    db.session.commit()
    logging.info('click - {}'.format(link_id))
    if len(link_id) == 4:
        return cut(link_id)
    else:
        return tree(link_id, db)


@application.route('/your_tree_link', methods=['POST', 'GET'])
def your_tree_link():
    personal_hash = create_multilink(request, db)
    return render_template('multilink.html',
                           forward_message=f'{personal_hash}')
