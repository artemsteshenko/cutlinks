from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import render_template, redirect
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import uuid
import json
import logging

from app.models import Users, Links


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


def tree(link_id, db):
    # to do: сделать норм названия
    page_name, desc, goods, links = parse_multilink(db, link_id)
    return render_template('profile.html', name=page_name,
                           desc=desc, links=links, goods=goods)


def cut(link_id):
    # to do: сделать норм названия
    link = Links.query.filter_by(link_id=link_id).first()
    if link is None:
        return '<h3>Нет такой короткой ссылки</h3>'
    logging.info('link - {}'.format(link.link))
    return redirect(link.link, code=302)


def number_clicks_plot(clicks_series):
    y_per = clicks_series / clicks_series.sum() * 100
    y = clicks_series
    x = clicks_series.index

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=y_per,
        y=x,
        marker=dict(
            color='rgb(116, 158, 170)',
            line=dict(
                color='rgb(116, 158, 170)',
                width=1),
        ),
        name='Отношение кликов за день к кликам за всю историю по ссылке',
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=y, y=x,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Количество кликов по ссылке',
    ), 1, 2)

    fig.update_layout(
        title='Статистика кликов по ссылке',
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.47, 1],
            side='top',
            dtick=1,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor='rgb(256, 256, 256)',
        plot_bgcolor='rgb(245, 240, 250)',
    )

    annotations = []

    y_s = np.round(y_per, decimals=2)
    y_nw = np.rint(y)

    # Adding labels
    for ydn, yd, xd in zip(y_nw, y_s, x):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn,
                                text='{:,}'.format(ydn) + '        ',
                                font=dict(family='Arial', size=12,
                                          color='rgb(128, 0, 128)'),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 3,
                                text=str(yd) + '%',
                                font=dict(family='Arial', size=12,
                                          color='rgb(116, 158, 170)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=-0.109,
                            text='',
                            font=dict(family='Arial', size=10,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig


def create_multilink(request, db):
    logging.info(request.form)
    page_name = request.form['page_name_0']
    links = request.form.to_dict()
    logging.info(links)
    links = json.dumps(links, ensure_ascii=False)

    hash = uuid.uuid4().hex[:6]
    username = 'site'

    cursor = db.cursor()
    cursor.execute(f"""INSERT treelinks(link_id, name,  link, username)
         VALUES ('{hash}','{page_name}', '{links}', '{username}')""")
    db.commit()
    cursor.close()
    return hash


def parse_multilink(db, link_id):
    # Выглядит как лютый треш
    db.reconnect()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM treelinks"
                   f" where link_id = '{link_id}'")
    multilinks_all = cursor.fetchall()
    cursor.close()
    if len(multilinks_all) == 0:
        return '<h3>Нет такой мульти ссылки</h3>'

    logging.info(multilinks_all)
    desc = 'Описание страницы'
    page_name = multilinks_all[0][2]
    elements = json.loads(multilinks_all[0][1])

    link_names, links = [], []
    good_names, good_descs, good_prices, good_link_buys = [], [], [], []
    for el in elements:
        logging.info(el)
        if el[:9] == 'link_name':
            link_names.append(elements[el])
        elif el[:4] == 'link':
            links.append(elements[el])
        elif el[:4] == 'desc':
            desc = elements[el]
        elif el[:9] == 'good_name':
            good_names.append(elements[el])
        elif el[:9] == 'good_desc':
            good_descs.append(elements[el])
        elif el[:10] == 'good_price':
            good_prices.append(elements[el])
        elif el[:13] == 'good_link_buy':
            good_link_buys.append(elements[el])
    dict_links = dict(zip(link_names, links))
    dict_goods = {i: [j, k, s, h] for i, j, k, s, h in
                  zip(range(len(good_names)), good_names, good_descs, good_prices, good_link_buys)}
    logging.info(dict_links)
    logging.info(dict_goods)
    return page_name, desc, dict_goods, dict_links
