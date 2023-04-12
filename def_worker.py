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
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute(
        'SELECT ID_Entities FROM Employees_Entities WHERE Passport_SN_Employees=?', (login,))
    c1 = c.fetchall()
    for row in c1:
        c.execute('SELECT * FROM Entities WHERE ID=?', (row[0],))
        name_ent = c.fetchone()[1]
        sq_ent = c.fetchone()[2]
        add_ent = c.fetchone()[3]
        User = Query()
        search = ord_db.search(User.id == row[0])
        for s in search:
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
            if s['status'] == 'not completed':
                res += f'Заказ {num}\n{name_ent}, {add_ent}, {sq_ent} кв. м\nУслуга 1: {s1}, {d1}, {t1}\nУслуга 2: {s2}, {d2}, {t2}\nУслуга 3: {s3}, {d3}, {t3}\n\n'
    c.execute(
        'SELECT Passport_SN_Individuals FROM Employees_Individuals WHERE Passport_SN_Employees=?', (login,))
    c2 = c.fetchall()
    for row in c2:
        c.execute(
            'SELECT * FROM Individuals WHERE Passport_SN=?', (row[0],))
        fname_ind = c.fetchone()[1]
        sname_ind = c.fetchone()[2]
        lname_ind = c.fetchone()[3]
        sq_ind = c.fetchone()[5]
        add_ind = c.fetchone()[4]
        User = Query()
        search = ord_db.search(User.id == row[0])
        for s in search:
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
            if s['status'] == 'not completed':
                res += f'Заказ {num}\n{lname_ind} {fname_ind} {sname_ind}, {add_ind}, {sq_ind} кв. м\nУслуга 1: {s1}, {d1}, {t1}\nУслуга 2: {s2}, {d2}, {t2}\nУслуга 3: {s3}, {d3}, {t3}\n\n'
    res = res[:-4:]
    window['-ASSIGN-'].update(res)
    conn.close()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Выйти':
            break

    window.close()
