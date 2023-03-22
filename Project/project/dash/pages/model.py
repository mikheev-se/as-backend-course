import dash
from dash import html, dcc
from project.dash.utils import token
import plotly.express as px

dash.register_page(__name__, title='Обучение и получение предсказаний')


def layout():
    if not token.token:
        return html.Div(dcc.Link(children='Вы не авторизованы. Нажмите, чтобы авторизоваться', href='/auth'))
    return html.Div(
        [
            html.H2(children='Обучение и получение предсказаний'),
            html.P('На данной странице можно инициировать обучение модели и просмотреть на графике предсказания по хранящимся на сервере данных.'),
            html.Button('FIT-PREDICT', id='fit-button'),
            dcc.Graph(id='fit-graph', figure=px.line()),
        ]
    )
