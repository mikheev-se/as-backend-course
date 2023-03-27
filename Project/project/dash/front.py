import base64
from dash import Dash, html, dcc, Input, Output
import dash
import plotly.express as px
import plotly.graph_objs as go
import flask
import requests
from io import BytesIO, StringIO
from project.dash.utils import API_URL, get_auth_header, token
import pandas as pd

stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'http://localhost:8050/static/styles.css'
]

app = Dash(__name__, use_pages=True, external_stylesheets=stylesheets,
           suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('Интерактивный дашборд'),

    html.Div([
        html.Nav(
            [html.P('Страницы')] + [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ],
            className='navbar'
        ),
        dcc.Loading(dash.page_container,
                    parent_className='page-content')
    ],
        className='content'
    )
], id='root')


@app.server.route('/api/users/authorize', methods=['POST'])
def auth():
    data = flask.request.form
    res = requests.post(API_URL + 'users/authorize', data=data)
    match res.status_code:
        case 200:
            token.token = res.json()['access_token']
        case 401:
            pass
    return flask.redirect('/auth')


@app.server.route('/api/users/register', methods=['POST'])
def register():
    data = flask.request.form
    res = requests.post(API_URL + 'users/register', json=dict(data))
    match res.status_code:
        case 201:
            res = requests.post(API_URL + 'users/authorize', data=data)
            token.token = res.json()['access_token']
        case 403:
            return flask.redirect('/register')
    return flask.redirect('/auth')


@app.server.route('/api/model/prepare')
def download():
    res = requests.get(API_URL + 'model/prepare', headers=get_auth_header())
    match res.status_code:
        case 200:
            return flask.send_file(BytesIO(res.content), download_name='prepared.csv')
        case 401:
            token.token = ''
            return app.server.make_response(flask.redirect('/auth'))
    return flask.redirect('/dataset')


@app.callback(Output('fit-graph', 'figure'), Input('fit-button', 'n_clicks'))
def fit_render(n_clicks: int):
    if n_clicks:
        res = requests.post(API_URL + 'model/fit', headers=get_auth_header())
        match res.status_code:
            case 202:
                res = requests.post(API_URL + 'model/predict',
                                    headers=get_auth_header())
                rows = StringIO(res.content.decode())
                df = pd.read_csv(rows, sep=';')
                fig = px.line(df, title='Значения целевого признака')

                return fig
            case 401:
                token.token = ''
                app.server.make_response(flask.redirect('/auth'))

    return px.line()


@app.callback(Output('evaluate-graph', 'figure'), Input('upload-data', 'contents'), Input('upload-data', 'filename'))
def parse_contents(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string).decode()
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(StringIO(decoded), sep=';')
            res = requests.post(API_URL + 'model/predict', files={
                                'upload_file': ('upload.csv', decoded)}, headers=get_auth_header())

            match res.status_code:
                case 200:

                    new_df = pd.read_csv(
                        StringIO(res.content.decode()), sep=';')
                    new_df.columns = ['pred']
                    fig = px.line(new_df, title='Значения целевого признака')
                    new_df['true'] = df['MMTCO2E'].values.flatten()
                    fig.add_trace(
                        go.Scatter(
                            x=list(new_df.index),
                            y=new_df['true'].values.flatten(),
                            mode='lines',
                            line={
                                'color': 'rgba(239, 86, 58, 0.7)'
                            },
                            name='true'
                        ),
                    )

                    return fig

                case 401:
                    token.token = ''
                    app.server.make_response(flask.redirect('/auth'))

    return px.line()


if __name__ == '__main__':
    app.run_server(debug=True)
