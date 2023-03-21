import dash
from dash import html, dcc, dash_table
import requests
from project.dash.utils import API_URL, get_auth_header, token

dash.register_page(__name__)


def layout():
    res = requests.get(API_URL + 'users/me',
                       headers=get_auth_header())
    if res.status_code == 200:
        user = res.json()
        return html.Div([
            html.H3(f'Добро пожаловать, {user["username"]}!'),
            html.P(f'Ваша роль: {user["role"]}')
        ])

    return html.Div(
        html.Form(
            children=[
                dcc.Input(placeholder='Login', name='username', value=''),
                dcc.Input(placeholder='Password',
                          type='password', name='password', value=''),
                html.Button(children='Sign in', type='submit')],
            action='api/users/authorize',
            method='post',
            className='auth-form'
        )
    )
