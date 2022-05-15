import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def number_clicks_plot(clicks_Series):
    y_per = clicks_Series/clicks_Series.sum() * 100
    y = clicks_Series
    x = clicks_Series.index


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
        title=f'Статистика кликов по ссылке',
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
                            font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig