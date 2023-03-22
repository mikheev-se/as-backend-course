import dash
from dash import html, dcc, dash_table
import requests
from project.dash.utils import API_URL, get_auth_header, token

dash.register_page(__name__, title='Авторизация')


def layout():
    res = requests.get(API_URL + 'users/me',
                       headers=get_auth_header())
    if res.status_code == 200:
        user = res.json()
        return html.Div([
            html.H3(f'Добро пожаловать, {user["username"]}!'),
            html.P(f'Ваша роль: {user["role"]}'),
            html.P(
                f'Дата регистрации: {user["created_at"]}') if user["created_at"] else None
        ])

    return html.Div(
        [
            html.H2(children='Авторизация'),
            html.Form(
                children=[
                    dcc.Input(placeholder='Логин', name='username', value=''),
                    dcc.Input(placeholder='Пароль',
                              type='password', name='password', value=''),
                    html.Button(children='Войти', type='submit')],
                action='api/users/authorize',
                method='post',
                className='auth-form'
            )
        ]
    )
