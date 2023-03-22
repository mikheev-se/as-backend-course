import dash
from dash import html, dcc
from project.dash.utils import token

dash.register_page(__name__, title='Оценка качества модели')


def layout():
    if not token.token:
        return html.Div(dcc.Link(children='Вы не авторизованы. Нажмите, чтобы авторизоваться', href='/auth'))
    return html.Div([
        html.H2(children='Оценка качества модели'),
        html.P('На данной странице можно загрузить свои данные, получить по ним предсказания и сравнить их с "настоящими" значениями на графике.'),
        html.P('Загруженные данные должны быть предобработаны. Также в них должен присутствовать целевой признак.'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Загрузите файлы или ',
                html.A('перетащите их сюда')
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
        dcc.Graph(id='evaluate-graph')
    ])
