import PySimpleGUI as sg
import sqlite3
import pickledb
from tinydb import TinyDB, Query
from datetime import date
from utils import *

rdb = pickledb.load('rates.db', False)
udb = pickledb.load('users.db', False)
ord_db = TinyDB('orders.db')


# Функция для регистрации физлица
def register_ind():
    layout = [
        [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
        [sg.Push(), sg.Text('Пароль:'), sg.InputText(
            key='-PASSIN-', password_char='*')],
        [sg.Push(), sg.Text('Серия и номер паспорта:'),
         sg.InputText(key='-PASSPORTSN-')],
        [sg.Push(), sg.Text('Фамилия:'), sg.InputText(key='-LNAME-')],
        [sg.Push(), sg.Text('Имя:'), sg.InputText(key='-FNAME-')],
        [sg.Push(), sg.Text('Отчество:'), sg.InputText(key='-SNAME-')],
        [sg.Push(), sg.Text('Адрес:'), sg.InputText(key='-ADDIN-')],
        [sg.Push(), sg.Text('Площадь помещения (кв. м):'),
         sg.InputText(key='-SQIN-')],
        [sg.Push(), sg.Button('Зарегистрироваться'),
         sg.Push(), sg.Button('Отмена')],
    ]

    window = sg.Window('Регистрация физического лица', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Отмена':
            break
        if event == 'Зарегистрироваться':
            try:
                ind = (
                    int(values['-PASSPORTSN-']),
                    str(values['-FNAME-']),
                    str(values['-SNAME-']),
                    str(values['-LNAME-']),
                    str(values['-ADDIN-']),
                    int(values['-SQIN-'])
                )
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    '''insert into Individuals (Passport_SN, F_Name, S_Name, L_Name, I_Address, Room_Square) values (?,?,?,?,?,?)''', ind)
                conn.commit()
                conn.close()
                udb.set(values['-LOGIN-'], [values['-PASSIN-'],
                        int(values['-PASSPORTSN-']), 'ind'])
                udb.dump()
                break
    window.close()


# Функция для регистрации юрлица
def register_ent():
    layout = [
        [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
        [sg.Push(), sg.Text('Пароль:'), sg.InputText(
            key='-PASSIN-', password_char='*')],
        [sg.Push(), sg.Text('Название организации:'),
         sg.InputText(key='-ENTNAME-')],
        [sg.Push(), sg.Text('Адрес:'), sg.InputText(key='-ADDENT-')],
        [sg.Push(), sg.Text('Площадь помещений (кв. м):'),
         sg.InputText(key='-SQENT-')],
        [sg.Push(), sg.Button('Зарегистрироваться'),
         sg.Push(), sg.Button('Отмена')],
    ]

    window = sg.Window('Регистрация юридического лица', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Отмена':
            break
        if event == 'Зарегистрироваться':
            try:
                ent = (
                    str(values['-ENTNAME-']),
                    int(values['-SQENT-']),
                    str(values['-ADDENT-'])
                )
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    '''insert into Entities (Naming, Square_Offices, E_Address) values (?,?,?)''', ent)
                conn.commit()
                conn.close()
                udb.set(values['-LOGIN-'], [values['-PASSIN-'],
                        str(values['-ENTNAME-']), 'ent'])
                udb.dump()
                break
    window.close()


# Функция для вывода окна пользователя
def user_window():
    layout_user = [
        [sg.Button('Создать заявку')],
        [sg.Button('Просмотреть мои заказы')],
        [sg.Button('Оставить отзыв')],
        [sg.Push(), sg.Button('Закрыть')]
    ]
    return sg.Window('Клининговая компания. Пользователь', layout_user)


# Функция для создания заказа физ. лица
def user_create_order_ind(login):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('SELECT Naming FROM C_Services')
    combo = []
    for serv in c.fetchall():
        combo.append(serv[0])
    conn.close()

    layout = [
        [sg.Text('Доступные услуги и их цена за кв. м:')],
        [sg.Multiline(key='-SERV-', size=(50, 5))],
        [sg.Text('Выберите до 3-х услуг для заказа:')],
        [sg.Push(), sg.Text('Услуга 1:'), sg.Combo(combo, key='-S1-'), sg.InputText(key='-D1-'), sg.CalendarButton('Выбрать дату',
                                                                                                                   close_when_date_chosen=True, target='-D1-', format='%Y-%m-%d'), sg.Text('Время (чч:мм):'), sg.InputText(key='-T1-')],
        [sg.Push(), sg.Text('Услуга 2:'), sg.Combo(combo, key='-S2-'), sg.InputText(key='-D2-'), sg.CalendarButton('Выбрать дату',
                                                                                                                   close_when_date_chosen=True, target='-D2-', format='%Y-%m-%d'), sg.Text('Время (чч:мм):'), sg.InputText(key='-T2-')],
        [sg.Push(), sg.Text('Услуга 3:'), sg.Combo(combo, key='-S3-'), sg.InputText(key='-D3-'), sg.CalendarButton('Выбрать дату',
                                                                                                                   close_when_date_chosen=True, target='-D3-', format='%Y-%m-%d'), sg.Text('Время (чч:мм):'), sg.InputText(key='-T3-')],
        [sg.Text('Стоимость услуг:'), sg.Text('0 руб.', key='-COST-')],
        [sg.Button('Создать заказ'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Создать заказ', layout, finalize=True)

    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    res_serv = 'Название Стоимость (кв. м)\n\n'
    c.execute('SELECT * FROM C_Services')
    serv = c.fetchall()
    for s in serv:
        res_serv += f'{s[1]} {s[2]}\n'
    window['-SERV-'].update(res_serv)
    conn.close()

    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Создать заказ':
            cost = 0
            id_work_spec = None
            id_order = None
            id_contract = None
            if values['-S1-'] and values['-D1-'] and values['-T1-']:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                          (values['-D1-'], values['-T1-'] + ':00'))
                c.execute('SELECT ID FROM Work_Spec WHERE W_Date=? AND W_Time=?',
                          (values['-D1-'], values['-T1-'] + ':00'))
                id_work_spec = c.fetchone()[0]
                c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                          (values['-S1-'],))
                id_work_type = c.fetchone()[0]
                c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                          (id_work_spec, id_work_type))
                c.execute('INSERT INTO Orders (ID_Work_Spec, O_Date) values (?,?)',
                          (id_work_spec, str(date.today())))
                c.execute(
                    'SELECT Number FROM Orders WHERE ID_Work_Spec=?', (id_work_spec,))
                id_order = c.fetchone()[0]
                contract = (
                    udb.get(login)[1],
                    'Договор оказания услуг',
                    str(date.today()),
                    id_order,
                    str(date.today()),
                    str(date.today())
                )
                c.execute(
                    'INSERT INTO Contracts (Passport_SN_Individuals, C_Name, Sign_Date, Number_Orders, Date_Start, Date_End) values (?,?,?,?,?,?)', contract)
                c.execute(
                    'SELECT Number FROM Contracts WHERE Number_Orders=?', (id_order,))
                id_contract = c.fetchone()[0]
                c.execute('SELECT ID FROM C_Services WHERE Naming=?',
                          (values['-S1-'],))
                id_serv = c.fetchone()[0]
                c.execute(
                    'insert into Contracts_C_Services (Number_Contracts, ID_C_Services) values (?,?)', (id_contract, id_serv))
                c.execute(
                    'SELECT Room_Square FROM Individuals WHERE Passport_SN=?', (udb.get(login)[1],))
                square = int(c.fetchone()[0])
                c.execute(
                    'SELECT I_Address FROM Individuals WHERE Passport_SN=?', (udb.get(login)[1],))
                address = c.fetchone()[0]
                c.execute(
                    'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S1-'],))
                cost += square * int(c.fetchone()[0])
                window['-COST-'].update(f'{cost} руб.')
                conn.commit()
                conn.close()
                if values['-S2-'] and values['-D2-'] and values['-T2-']:
                    conn = sqlite3.connect('Cleaning_Company.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                              (values['-D2-'], values['-T2-'] + ':00'))
                    c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                              (values['-S2-'],))
                    id_work_type = c.fetchone()[0]
                    c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                              (id_work_spec, id_work_type))
                    c.execute('SELECT ID FROM C_Services WHERE Naming=?',
                              (values['-S2-'],))
                    id_serv = c.fetchone()[0]
                    c.execute(
                        'insert into Contracts_C_Services (Number_Contracts, ID_C_Services) values (?,?)', (id_contract, id_serv))
                    c.execute(
                        'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S2-'],))
                    cost += square * int(c.fetchone()[0])
                    window['-COST-'].update(f'{cost} руб.')
                    conn.commit()
                    conn.close()
                if values['-S3-'] and values['-D3-'] and values['-T3-']:
                    conn = sqlite3.connect('Cleaning_Company.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                              (values['-D3-'], values['-T3-'] + ':00'))
                    c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                              (values['-S3-'],))
                    id_work_type = c.fetchone()[0]
                    c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                              (id_work_spec, id_work_type))
                    c.execute('SELECT ID FROM C_Services WHERE Naming=?',
                              (values['-S3-'],))
                    id_serv = c.fetchone()[0]
                    c.execute(
                        'insert into Contracts_C_Services (Number_Contracts, ID_C_Services) values (?,?)', (id_contract, id_serv))
                    c.execute(
                        'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S3-'],))
                    cost += square * int(c.fetchone()[0])
                    window['-COST-'].update(f'{cost} руб.')
                    conn.commit()
                    conn.close()
                sg.Popup(
                    f'Заказ создан успешно!\nНомер заказа: {id_order}\nСтоимость услуг: {cost} руб.', title='Успешно')
                ord_db.insert({
                    'login': login,
                    'id': udb.get(login)[1],
                    'S1': values['-S1-'], 'D1': values['-D1-'], 'T1': values['-T1-'] + ':00',
                    'S2': values['-S2-'], 'D2': values['-D2-'], 'T2': values['-T2-'] + ':00',
                    'S3': values['-S3-'], 'D3': values['-D3-'], 'T3': values['-T3-'] + ':00',
                    'num': id_order,
                    'square': square,
                    'address': address,
                    'cost': cost,
                    'wrk': 0,
                    'status': 'not completed'
                })
            else:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

    window.close()


# Функция для создания заказа юр. лица
def user_create_order_ent(login):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('SELECT Naming FROM C_Services')
    combo = []
    for serv in c.fetchall():
        combo.append(serv[0])
    conn.close()

    layout = [
        [sg.Text('Доступные услуги и их цена за кв. м:')],
        [sg.Multiline(key='-SERV-', size=(50, 5))],
        [sg.Text('Выберите до 3-х услуг для заказа:')],
        [sg.Push(), sg.Text('Услуга 1:'), sg.Combo(combo, key='-S1-'), sg.InputText(key='-D1-'), sg.CalendarButton('Выбрать дату',
                                                                                                                   close_when_date_chosen=True, target='-D1-', format='%Y-%m-%d'), sg.Text('Время (чч:мм):'), sg.InputText(key='-T1-')],
        [sg.Push(), sg.Text('Услуга 2:'), sg.Combo(combo, key='-S2-'), sg.InputText(key='-D2-'), sg.CalendarButton('Выбрать дату',
                                                                                                                   close_when_date_chosen=True, target='-D2-', format='%Y-%m-%d'), sg.Text('Время (чч:мм):'), sg.InputText(key='-T2-')],
        [sg.Push(), sg.Text('Услуга 3:'), sg.Combo(combo, key='-S3-'), sg.InputText(key='-D3-'), sg.CalendarButton('Выбрать дату',
                                                                                                                   close_when_date_chosen=True, target='-D3-', format='%Y-%m-%d'), sg.Text('Время (чч:мм):'), sg.InputText(key='-T3-')],
        [sg.Text('Стоимость услуг:'), sg.Text('0 руб.', key='-COST-')],
        [sg.Button('Создать заказ'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Создать заказ', layout, finalize=True)

    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    res_serv = 'Название Стоимость (кв. м)\n\n'
    c.execute('SELECT * FROM C_Services')
    serv = c.fetchall()
    for s in serv:
        res_serv += f'{s[1]} {s[2]}\n'
    window['-SERV-'].update(res_serv)
    conn.close()

    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Создать заказ':
            cost = 0
            id_work_spec = None
            id_order = None
            id_contract = None
            if values['-S1-'] and values['-D1-'] and values['-T1-']:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                          (values['-D1-'], values['-T1-'] + ':00'))
                c.execute('SELECT ID FROM Work_Spec WHERE W_Date=? AND W_Time=?',
                          (values['-D1-'], values['-T1-'] + ':00'))
                id_work_spec = c.fetchone()[0]
                c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                          (values['-S1-'],))
                id_work_type = c.fetchone()[0]
                c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                          (id_work_spec, id_work_type))
                c.execute('INSERT INTO Orders (ID_Work_Spec, O_Date) values (?,?)',
                          (id_work_spec, str(date.today())))
                c.execute(
                    'SELECT Number FROM Orders WHERE ID_Work_Spec=?', (id_work_spec,))
                id_order = c.fetchone()[0]
                ent_name = udb.get(login)[1]
                c.execute('SELECT ID FROM Entities WHERE Naming=?', (ent_name,))
                id_ent = int(c.fetchone()[0])
                contract = (
                    id_ent,
                    'Договор оказания услуг',
                    str(date.today()),
                    id_order,
                    str(date.today()),  # TODO
                    str(date.today())  # TODO
                )
                c.execute(
                    'INSERT INTO Contracts (ID_Entities, C_Name, Sign_Date, Number_Orders, Date_Start, Date_End) values (?,?,?,?,?,?)', contract)
                c.execute(
                    'SELECT Number FROM Contracts WHERE Number_Orders=?', (id_order,))
                id_contract = c.fetchone()[0]
                c.execute('SELECT ID FROM C_Services WHERE Naming=?',
                          (values['-S1-'],))
                id_serv = c.fetchone()[0]
                c.execute(
                    'insert into Contracts_C_Services (Number_Contracts, ID_C_Services) values (?,?)', (id_contract, id_serv))
                c.execute(
                    'SELECT Square_Offices FROM Entities WHERE ID=?', (id_ent,))
                square = int(c.fetchone()[0])
                c.execute(
                    'SELECT E_Address FROM Entities WHERE ID=?', (id_ent,))
                address = c.fetchone()[0]
                c.execute(
                    'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S1-'],))
                cost += square * int(c.fetchone()[0])
                window['-COST-'].update(f'{cost} руб.')
                conn.commit()
                conn.close()
                if values['-S2-'] and values['-D2-'] and values['-T2-']:
                    conn = sqlite3.connect('Cleaning_Company.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                              (values['-D2-'], values['-T2-'] + ':00'))
                    c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                              (values['-S2-'],))
                    id_work_type = c.fetchone()[0]
                    c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                              (id_work_spec, id_work_type))
                    c.execute('SELECT ID FROM C_Services WHERE Naming=?',
                              (values['-S2-'],))
                    id_serv = c.fetchone()[0]
                    c.execute(
                        'insert into Contracts_C_Services (Number_Contracts, ID_C_Services) values (?,?)', (id_contract, id_serv))
                    c.execute(
                        'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S2-'],))
                    cost += square * int(c.fetchone()[0])
                    window['-COST-'].update(f'{cost} руб.')
                    conn.commit()
                    conn.close()
                if values['-S3-'] and values['-D3-'] and values['-T3-']:
                    conn = sqlite3.connect('Cleaning_Company.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                              (values['-D3-'], values['-T3-'] + ':00'))
                    c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                              (values['-S3-'],))
                    id_work_type = c.fetchone()[0]
                    c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                              (id_work_spec, id_work_type))
                    c.execute('SELECT ID FROM C_Services WHERE Naming=?',
                              (values['-S3-'],))
                    id_serv = c.fetchone()[0]
                    c.execute(
                        'insert into Contracts_C_Services (Number_Contracts, ID_C_Services) values (?,?)', (id_contract, id_serv))
                    c.execute(
                        'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S3-'],))
                    cost += square * int(c.fetchone()[0])
                    window['-COST-'].update(f'{cost} руб.')
                    conn.commit()
                    conn.close()
                sg.Popup(
                    f'Заказ создан успешно!\nНомер заказа: {id_order}\nСтоимость услуг: {cost} руб.', title='Успешно')
                ord_db.insert({
                    'login': login,
                    'id': id_ent,
                    'S1': values['-S1-'], 'D1': values['-D1-'], 'T1': values['-T1-'] + ':00',
                    'S2': values['-S2-'], 'D2': values['-D2-'], 'T2': values['-T2-'] + ':00',
                    'S3': values['-S3-'], 'D3': values['-D3-'], 'T3': values['-T3-'] + ':00',
                    'num': id_order,
                    'square': square,
                    'address': address,
                    'cost': cost,
                    'wrk': 0,
                    'status': 'not completed'
                })
            else:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

    window.close()


# Функция для просмотра всех заказов пользователя
def user_list_orders(login):
    layout = [
        [sg.Text('Мои заказы:')],
        [sg.Multiline(key='-MYORD-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Мои заказы', layout, finalize=True)

    User = Query()
    my_orders = ord_db.search(User.login == login)
    if my_orders == []:
        window['-MYORD-'].update('Похоже, Вы еще не сделали ни одного заказа...')
    else:
        res = ''
        for mo in my_orders:
            res += f"Номер заказа: {mo['num']}\n"
            res += f"Услуга 1: {mo['S1']}, {mo['D1']}, {mo['T1']}\n"
            if mo['S2'] != '':
                res += f"Услуга 2: {mo['S2']}, {mo['D2']}, {mo['T2']}\n"
                if mo['S3'] != '':
                    res += f"Услуга 3: {mo['S3']}, {mo['D3']}, {mo['T3']}\n"
            res += f"Стоимость: {mo['cost']} руб.\n\n"

        window['-MYORD-'].update(res)

    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break

    window.close()


# Функция для обратной связи по заказу
def user_give_feedback():
    layout = [
        [sg.Text('Номер заказа:')],
        [sg.InputText(key='-ORDNUM-', do_not_clear=False)],
        [sg.Text(
            'Оцените услуги от 1 до 5, где 1 - очень плохо, 5 - очень хорошо')],
        [sg.Text('Качество работ:'), sg.Combo(
            ['5', '4', '3', '2', '1'], key='-CR1-', default_value='5')],
        [sg.Text('Комментарий:')],
        [sg.Multiline(key='-COMM-', size=(50, 5), do_not_clear=False)],
        [sg.Button('Оставить отзыв'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Оставить отзыв', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Оставить отзыв':
            rdb.set(values['-ORDNUM-'], [values['-CR1-'], values['-COMM-']])
            rdb.dump()
            sg.Popup('Отзыв оставлен успешно, спасибо!', title='Успешно')

    window.close()
