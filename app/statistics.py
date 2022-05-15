import json
import plotly
import pandas as pd
from flask import Blueprint, render_template, request

from utils import mydb
from statistic_plots import number_clicks_plot

statistic_blueprint = Blueprint('statistic', __name__)

@statistic_blueprint.route("/shortlink")
def statistic():
    return render_template('stat.html')


@statistic_blueprint.route('/stat', methods=['POST', 'GET'])
def stat():
    link = request.form['link']
    link_id = link.split('/')[-1]

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