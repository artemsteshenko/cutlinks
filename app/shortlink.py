from flask import Blueprint
from app import db
from app.models import Links
from flask import render_template, request
import uuid

shortlink_blueprint = Blueprint('shortlink', __name__)


@shortlink_blueprint.route("/shortlink")
def shortlink():
    return render_template('shortlink.html')


@shortlink_blueprint.route('/your_short_link', methods=['POST', 'GET'])
def your_short_link():
    link = request.form['link']
    pers_hash = uuid.uuid4().hex[:4]
    username = 'site'
    link = Links(link_id=pers_hash, link=link, username=username)
    db.session.add(link)
    db.session.commit()
    return render_template('shortlink.html',
                           forward_message=f'http://cutlinks.ru/{pers_hash}')
