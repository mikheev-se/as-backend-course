import dash
from dash import html, dcc
from project.dash.utils import token
import plotly.express as px

dash.register_page(__name__)


def layout():
    if not token.token:
        return html.Div(dcc.Link(children='Unauthorized. Click here to sign in', href='/auth'))
    return html.Div(
        [
            html.Button('FIT-PREDICT', id='fit-button'),
            dcc.Graph(id='fit-graph', figure=px.line([1, 2])),
        ]
    )
