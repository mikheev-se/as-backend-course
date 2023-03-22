from io import StringIO
import dash
from dash import html, dcc, dash_table
import flask
import requests
from project.dash.utils import API_URL, get_auth_header, token
import pandas as pd

dash.register_page(__name__, title='Датасет')


def layout():
    if not token.token:
        return html.Div(dcc.Link(children='Вы не авторизованы. Нажмите, чтобы авторизоваться', href='/auth'))

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
                html.H2(children='Датасет'),
                html.P('Описание датасета: Этот набор данных является дополнением к исследованию технологического тепла на уровне предприятия, ' +
                       'проведенному McMillan et al в 2015 году. Используя ту же методологию, годовое потребление энергии при сжигании ' +
                       'на установке было рассчитано на основе данных о выбросах, представленных в Программу отчетности Агентства по охране окружающей среды США ' +
                       'по парниковым газам за 2010-2015 годы. Итоговые значения энергии в ТДЖ в целом и по видам топлива были дополнительно охарактеризованы ' +
                       'по конечному потреблению с использованием данных Обследования энергопотребления на производстве Управления энергетической информации США ' +
                       'за 2010 год и по диапазону температур. Набор данных включает рассчитанные выбросы парниковых газов в млн тонн CO2e в разбивке по типу ' +
                       'конечного использования топлива и диапазону температур.'),
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
