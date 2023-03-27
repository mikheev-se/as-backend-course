import dash
from dash import html, dcc


dash.register_page(__name__, title='Регистрация')


def layout():

    return html.Div(
        [
            html.H2(children='Регистрация'),
            html.Form(
                children=[
                    dcc.Input(placeholder='Логин', name='username', value=''),
                    dcc.Input(placeholder='Пароль',
                              type='password', name='password', value=''),
                    html.Button(children='Зарегистрироваться', type='submit')],
                action='api/users/register',
                method='post',
                className='auth-form'
            )
        ]
    )
