import PySimpleGUI as sg
import sqlite3
import pickledb
from tinydb import TinyDB, Query
from utils import *

rdb = pickledb.load('rates.db', False)
udb = pickledb.load('users.db', False)
ord_db = TinyDB('orders.db')


# Функция для вывода окна сотрудника
def worker_window(login):
    layout_worker = [
        [sg.Text('Мои назначения:')],
        [sg.Multiline(key='-ASSIGN-', size=(50, 5))],
        [sg.Push(), sg.Button('Выйти')]
    ]

    window = sg.Window('Клининговая компания. Сотрудник',
                       layout_worker, finalize=True)

    res = ''
    User = Query()
    search = ord_db.search(User.wrk == int(login))
    for s in search:
        sq = s['square']
        add = s['address']
        num = s['num']
        s1 = s['S1']
        d1 = s['D1']
        t1 = s['T1']
        s2 = s['S2']
        d2 = s['D2']
        t2 = s['T2']
        s3 = s['S3']
        d3 = s['D3']
        t3 = s['T3']
        if s['status'] == 'assigned':
            res += f'Заказ {num}\n{add}, {sq} кв. м\nУслуга 1: {s1}, {d1}, {t1}\n'
            if s2 != '':
                res += f'Услуга 2: {s2}, {d2}, {t2}\n'
                if s3 != '':
                    res += f'Услуга 3: {s3}, {d3}, {t3}\n'
            res += '\n'
    window['-ASSIGN-'].update(res)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Выйти':
            break

    window.close()
