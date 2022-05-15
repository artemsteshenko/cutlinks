from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template
import mysql.connector

from parse_multilink import parse_multilink


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


mydb = mysql.connector.connect(
  database='u1650045_default',
  host="cutlinks.ru",
  user="u1650045_default",
  password="mqGIBF31HU1x8zxo"
)


def tree(link_id):
    page_name, desc, goods, links = parse_multilink(mydb, link_id)
    return render_template('profile.html', name=page_name, desc=desc, links=links, goods=goods)