from io import StringIO
import dash
from dash import html, dcc, dash_table
import flask
import requests
from project.dash.utils import API_URL, get_auth_header, token
import pandas as pd

dash.register_page(__name__)


def layout():
    if not token.token:
        return html.Div(dcc.Link(children='Unauthorized. Click here to sign in', href='/auth'))

    res = requests.get(API_URL + 'model/download',
                       headers=get_auth_header())
    # rows = res.content.decode().split('\n')
    match res.status_code:
        case 200:
            rows = StringIO(res.content.decode())
            # df = pd.DataFrame([row.split(';')
            #                    for row in rows[1:]], columns=rows[0].split(';'))[:-1]
            df = pd.read_csv(rows, sep=';')
            df = df.head(1000)
            return html.Div([
                dash_table.DataTable(
                    df.to_dict('records'), [{"name": i, "id": i, "hideable": True}
                                            for i in df.columns],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    id='datatable',
                ),
                # dcc.Checklist(cols, cols,
                #               inline=True,
                #               id='cols-checklist'),
                html.Form(
                    html.Button('Предобработать'),
                    action='/api/model/prepare',
                )
            ])
        case 401:
            token.token = ''
            flask.redirect('/auth')

    return 'Unauthorized'
