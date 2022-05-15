import uuid
import json
import logging

from flask import Flask, redirect, render_template, request
import pandas as pd
import plotly

from statistic_plots import number_clicks_plot
from utils import LoginForm, mydb, tree
from parse_multilink import create_multilink


application = Flask(__name__)
application.config['SECRET_KEY'] = 'some-easy-key'

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


@application.route('/stat', methods=['POST', 'GET'])
def stat():
    link = request.form['link']
    link_id = link.split('/')[-1]
    logging.info(link_id)

    cursor = mydb.cursor()
    cursor.execute(f"SELECT created_at FROM clicks where link = '{link_id}'")
    myresult = cursor.fetchall()
    cursor.close()

    if len(myresult) == 0:
        return '<h3>Нет кликов</h3>'

    clicks = [click[0] for click in myresult]
    clicks_Series = pd.Series(clicks).dt.normalize().value_counts().sort_index()
    fig = number_clicks_plot(clicks_Series)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('notdash.html', graphJSON=graphJSON, link=link)


@application.route('/shortlink')
def shortlink():
    return render_template('shortlink.html')


@application.route('/multilink')
def multilink():
    return render_template('multilink.html')


def cut(link_id):
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM links where link_id = '{link_id}'")
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return '<h3>Нет такой короткой ссылки</h3>'
    return redirect(myresult[0][1], code=302)


@application.route("/<link_id>")
def multiple(link_id):
    cursor = mydb.cursor()
    cursor.execute(f"""INSERT clicks(link) VALUES ('{link_id}')""")
    mydb.commit()
    cursor.close()

    if len(link_id) == 4:
        return cut(link_id)
    else:
        return tree(link_id)


@application.route('/your_short_link', methods=['POST', 'GET'])
def your_short_link():
    link = request.form['link']
    hash = uuid.uuid4().hex[:4]
    username = 'site'

    cursor = mydb.cursor()
    cursor.execute(f"""INSERT links(link_id, link, username) VALUES ('{hash}', '{link}', '{username}')""")
    mydb.commit()
    cursor.close()

    return render_template('shortlink.html', forward_message=f'http://cutlinks.ru/{hash}')


@application.route('/your_tree_link', methods=['POST', 'GET'])
def your_tree_link():
    hash = create_multilink(request, mydb)
    return render_template('multilink.html', forward_message=f'{hash}')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
