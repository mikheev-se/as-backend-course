import dash
from dash import html, dcc
from project.dash.utils import token

dash.register_page(__name__)


def layout():
    if not token.token:
        return html.Div(dcc.Link(children='Unauthorized. Click here to sign in', href='/auth'))
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
        html.Div(id='output-data-upload'),
        dcc.Graph(id='evaluate-graph')
    ])
