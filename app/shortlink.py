from flask import Blueprint, render_template

shortlink_blueprint = Blueprint('shortlink', __name__)

@shortlink_blueprint.route("/shortlink")
def shortlink():
    return render_template('shortlink.html')

