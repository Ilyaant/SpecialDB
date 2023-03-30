import PySimpleGUI as sg
import sqlite3
import pickledb
from tinydb import TinyDB
from datetime import date

rdb = pickledb.load('rates.db', False)
udb = pickledb.load('users.db', False)
ord_db = TinyDB('orders.db')

######################################## ADMIN ######################################################


# Функция для вывода окна админа
def admin_window():
    layout_admin = [
        [sg.Button('Добавить услугу'), sg.Push(),
         sg.Button('Просмотреть клиентов')],
        [sg.Button('Добавить тип работ'), sg.Push(),
         sg.Button('Просмотреть сотрудников')],
        [sg.Button('Добавить должность'), sg.Push(),
         sg.Button('Просмотреть договоры')],
        [sg.Button('Добавить сотрудника'), sg.Push(),
         sg.Button('Просмотреть заказы')],
        [sg.Button('Назначить сотрудника')],
        [sg.Push(), sg.Button('Выйти')]
    ]
    return sg.Window('Клининговая компания. Администратор', layout_admin)


def admin_add_service():
    layout = [
        [sg.Text('Название услуги:')],
        [sg.InputText(key='-SNAME-')],
        [sg.Text('Цена за квадратный метр или единицу:')],
        [sg.InputText(key='-SCOST-')],
        [sg.Button('Добавить'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Добавить услугу', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Добавить':
            try:
                serv = (values['-SNAME-'], int(values['-SCOST-']), 0)
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'INSERT INTO C_Services (Naming, Cost_m2, Popularity) VALUES (?,?,?)', serv)
                c.execute('INSERT INTO Work_Types (Naming) values (?)',
                          (values['-SNAME-'],))
                conn.commit()
                conn.close()
                break
    window.close()


def admin_add_work_type():
    layout = [
        [sg.Text('Название типа работ:')],
        [sg.InputText(key='-WTNAME-')],
        [sg.Button('Добавить'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Добавить тип работ', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Добавить':
            conn = sqlite3.connect('Cleaning_Company.db')
            c = conn.cursor()
            c.execute(
                'INSERT INTO Work_Types (Naming) VALUES (?)', (values['-WTNAME-'],))
            conn.commit()
            conn.close()
            break
    window.close()


def admin_add_position():
    layout = [
        [sg.Text('Название должности:')],
        [sg.InputText(key='-PNAME-')],
        [sg.Text('Заработная плата:')],
        [sg.InputText(key='-PCOST-')],
        [sg.Button('Добавить'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Добавить должность', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Добавить':
            try:
                pos = (values['-PNAME-'], int(values['-PCOST-']))
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'INSERT INTO Positions (Naming, Salary) VALUES (?,?)', pos)
                conn.commit()
                conn.close()
                break
    window.close()


def admin_add_worker():
    layout = [
        [sg.Text('Серия и номер паспорта:')],
        [sg.InputText(key='-WSN-')],
        [sg.Text('Должность:')],
        [sg.InputText(key='-WPOS-')],
        [sg.Text('Имя:')],
        [sg.InputText(key='-WFNAME-')],
        [sg.Text('Отчество:')],
        [sg.InputText(key='-WSNAME-')],
        [sg.Text('Фамилия:')],
        [sg.InputText(key='-WLNAME-')],
        [sg.Text('Дата рождения:')],
        [sg.InputText(key='-WBDATE-'), sg.CalendarButton('Выбрать дату',
                                                         close_when_date_chosen=True, target='-WBDATE-', format='%Y-%m-%d')],
        [sg.Text('Дата приема на работу:')],
        [sg.InputText(key='-WHDATE-'), sg.CalendarButton('Выбрать дату',
                                                         close_when_date_chosen=True, target='-WHDATE-', format='%Y-%m-%d')],
        [sg.Button('Добавить'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Добавить сотрудника', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Добавить':
            try:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                id_pos = None
                for row in c.execute("SELECT * FROM Positions WHERE Naming=?", (values['-WPOS-'])):
                    id_pos = row[0]
                worker = (int(values['-WSN-']), id_pos, values['-WFNAME-'],
                          values['-WSNAME-'], values['-WLNAME-'], values['-WBDATE-'], values['-WHDATE-'])
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'INSERT INTO Employees (Passport_SN, ID_Positions, F_Name, S_Name, L_Name, Date_Birth, Date_hire) VALUES (?,?,?,?,?,?,?)', worker)
                conn.commit()
                conn.close()
                udb.set(values['-WSN-'], [values['-WLNAME-'], 'wrk'])
                udb.dump()
                break
    window.close()


def admin_list_clients():
    layout = [
        [sg.Text('Физические лица:')],
        [sg.Multiline(key='-IND-', size=(50, 5))],
        [sg.Text('Юридические лица:')],
        [sg.Multiline(key='-ENT-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть клиентов', layout)
    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break
        conn = sqlite3.connect('Cleaning_Company.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Individuals')
        window['-IND-'].update(c.fetchall())
        c.execute('SELECT * FROM Entities')
        window['-ENT-'].update(c.fetchall())
        conn.close()
    window.close()


def admin_list_workers():
    layout = [
        [sg.Text('Сотрудники:')],
        [sg.Multiline(key='-EMP-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть сотрудников', layout)
    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break
        conn = sqlite3.connect('Cleaning_Company.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Employees')
        window['-EMP-'].update(c.fetchall())
        conn.close()
    window.close()


def admin_list_contracts():
    layout = [
        [sg.Text('Договоры:')],
        [sg.Multiline(key='-CON-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть договоры', layout)
    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break
        conn = sqlite3.connect('Cleaning_Company.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Contracts')
        window['-CON-'].update(c.fetchall())
        conn.close()
    window.close()


def admin_list_orders():
    layout = [
        [sg.Text('Заказы:')],
        [sg.Multiline(key='-ORD-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть заказы', layout)
    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break
        conn = sqlite3.connect('Cleaning_Company.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Orders')
        window['-ORD-'].update(c.fetchall())
        conn.close()
    window.close()


def admin_assign_worker():
    # TODO
    return 0

######################################## USER ######################################################


# Функция для регистрации физлица
def register_ind():
    layout = [
        [sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
        [sg.Text('Пароль:'), sg.InputText(key='-PASSIN-', password_char='*')],
        [sg.Text('Серия и номер паспорта:'), sg.InputText(key='-PASSPORTSN-')],
        [sg.Text('Фамилия:'), sg.InputText(key='-LNAME-')],
        [sg.Text('Имя:'), sg.InputText(key='-FNAME-')],
        [sg.Text('Отчество:'), sg.InputText(key='-SNAME-')],
        [sg.Text('Адрес:'), sg.InputText(key='-ADDIN-')],
        [sg.Text('Площадь помещения (кв. м):'), sg.InputText(key='-SQIN-')],
        [sg.Button('Зарегистрироваться'), sg.Push(), sg.Button('Отмена')],
    ]

    window = sg.window('Регистрация физического лица', layout)
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


# Функция для регистрации юрлица
def register_ent():
    layout = [
        [sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
        [sg.Text('Пароль:'), sg.InputText(key='-PASSIN-', password_char='*')],
        [sg.Text('Название организации:'), sg.InputText(key='-ENTNAME-')],
        [sg.Text('Адрес:'), sg.InputText(key='-ADDENT-')],
        [sg.Text('Площадь помещений (кв. м):'), sg.InputText(key='-SQENT-')],
        [sg.Button('Зарегистрироваться'), sg.Push(), sg.Button('Отмена')],
    ]

    window = sg.window('Регистрация юридического лица', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Отмена':
            break
        if event == 'Зарегистрироваться':
            try:
                ent = (
                    str(values['-ENTNAME-']),
                    str(values['-ADDENT-']),
                    int(values['-SQENT-'])
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


# Функция для вывода окна пользователя
def user_window():
    layout_user = [
        [sg.Button('Создать заявку')],
        [sg.Button('Просмотреть мои заявки')],
        [sg.Button('Оставить отзыв')],
        [sg.Push(), sg.Button('Закрыть')]
    ]
    return sg.Window('Клининговая компания. Пользователь', layout_user)


def user_create_order_ind(login):
    layout = [
        [sg.Text('Доступные услуги и их цена за кв. м:')],
        [sg.Multiline(key='-SERV-', size=(50, 5))],
        [sg.Text('Выберите до 3-х услуг для заказа:')],
        [sg.Push(), sg.Text('Услуга 1:'), sg.InputText(key='-S1-'), sg.InputText(key='-D1-'), sg.CalendarButton('Выбрать дату',
                                                                                                                close_when_date_chosen=True, target='-D1-', format='%Y-%m-%d'), sg.Text('Время (чч:мм:сс):'), sg.InputText(key='-T1-')],
        [sg.Push(), sg.Text('Услуга 2:'), sg.InputText(key='-S2-'), sg.InputText(key='-D2-'), sg.CalendarButton('Выбрать дату',
                                                                                                                close_when_date_chosen=True, target='-D2-', format='%Y-%m-%d'), sg.Text('Время (чч:мм:сс):'), sg.InputText(key='-T2-')],
        [sg.Push(), sg.Text('Услуга 3:'), sg.InputText(key='-S3-'), sg.InputText(key='-D3-'), sg.CalendarButton('Выбрать дату',
                                                                                                                close_when_date_chosen=True, target='-D3-', format='%Y-%m-%d'), sg.Text('Время (чч:мм:сс):'), sg.InputText(key='-T3-')],
        [sg.Text('Стоимость услуг:'), sg.Text('0', key='-COST-')],
        [sg.Button('Создать заказ'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Создать заказ', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        conn = sqlite3.connect('Cleaning_Company.db')
        c = conn.cursor()
        c.execute('SELECT * FROM C_Services')
        window['-SERV-'].update(c.fetchall())
        conn.close()

        if event == 'Создать заказ':
            cost = 0
            id_work_spec = None
            id_order = None
            id_contract = None
            if values['-S1-'] and values['-D1-'] and values['-T1-']:
                c = conn.cursor()
                c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                          (values['-D1-'], values['-T1-']))
                c.execute('SELECT ID FROM Work_Spec WHERE W_Date=? AND W_Time=?',
                          (values['-D1-'], values['-T1-']))
                id_work_spec = c.fetchone()[0]
                c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                          (values['-S1-'],))
                id_work_type = c.fetchone()[0]
                c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                          (id_work_spec, id_work_type))
                c.execute('INSERT INTO Orders (ID_Work_Spec, O_Date) values (?,?)',
                          (id_work_spec, str(date.today())))
                c.execute(
                    'SELECT ID FROM Orders WHERE ID_Work_Spec=?', (id_work_spec,))
                id_order = c.fetchone()[0]
                contract = (
                    udb.get(login)[1],
                    'Договор оказания услуг',
                    str(date.today()),
                    id_order,
                    str(date.today()),  # TODO
                    str(date.today())  # TODO
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
                    'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S1-'],))
                cost += square * int(c.fetchone()[0])
                window['-COST-'].update(cost)
                conn.commit()
                conn.close()
                if values['-S2-'] and values['-D2-'] and values['-T2-']:
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (ID, W_Date, W_Time) values (?,?,?)',
                              (id_work_spec, values['-D2-'], values['-T2-']))
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
                    window['-COST-'].update(cost)
                    conn.commit()
                    conn.close()
                if values['-S3-'] and values['-D3-'] and values['-T3-']:
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (ID, W_Date, W_Time) values (?,?,?)',
                              (id_work_spec, values['-D3-'], values['-T3-']))
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
                    window['-COST-'].update(cost)
                    conn.commit()
                    conn.close()
                sg.Popup(
                    f'Заказ создан успешно!\nНомер заказа: {id_order}\nНомер договора: {id_contract}\nСтоимость услуг: {cost}', title='Успешно')
            else:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

    window.close()


def user_create_order_ent(login):
    layout = [
        [sg.Text('Доступные услуги и их цена за кв. м:')],
        [sg.Multiline(key='-SERV-', size=(50, 5))],
        [sg.Text('Выберите до 3-х услуг для заказа:')],
        [sg.Push(), sg.Text('Услуга 1:'), sg.InputText(key='-S1-'), sg.InputText(key='-D1-'), sg.CalendarButton('Выбрать дату',
                                                                                                                close_when_date_chosen=True, target='-D1-', format='%Y-%m-%d'), sg.Text('Время (чч:мм:сс):'), sg.InputText(key='-T1-')],
        [sg.Push(), sg.Text('Услуга 2:'), sg.InputText(key='-S2-'), sg.InputText(key='-D2-'), sg.CalendarButton('Выбрать дату',
                                                                                                                close_when_date_chosen=True, target='-D2-', format='%Y-%m-%d'), sg.Text('Время (чч:мм:сс):'), sg.InputText(key='-T2-')],
        [sg.Push(), sg.Text('Услуга 3:'), sg.InputText(key='-S3-'), sg.InputText(key='-D3-'), sg.CalendarButton('Выбрать дату',
                                                                                                                close_when_date_chosen=True, target='-D3-', format='%Y-%m-%d'), sg.Text('Время (чч:мм:сс):'), sg.InputText(key='-T3-')],
        [sg.Text('Стоимость услуг:'), sg.Text('0', key='-COST-')],
        [sg.Button('Создать заказ'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Создать заказ', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        conn = sqlite3.connect('Cleaning_Company.db')
        c = conn.cursor()
        c.execute('SELECT * FROM C_Services')
        window['-SERV-'].update(c.fetchall())
        conn.close()

        if event == 'Создать заказ':
            cost = 0
            id_work_spec = None
            id_order = None
            id_contract = None
            if values['-S1-'] and values['-D1-'] and values['-T1-']:
                c = conn.cursor()
                c.execute('INSERT INTO Work_Spec (W_Date, W_Time) values (?,?)',
                          (values['-D1-'], values['-T1-']))
                c.execute('SELECT ID FROM Work_Spec WHERE W_Date=? AND W_Time=?',
                          (values['-D1-'], values['-T1-']))
                id_work_spec = c.fetchone()[0]
                c.execute('SELECT ID FROM Work_Types WHERE Naming=?',
                          (values['-S1-'],))
                id_work_type = c.fetchone()[0]
                c.execute('INSERT INTO Work_Spec_Work_Types (ID_Work_Spec, ID_Work_Types) values (?,?)',
                          (id_work_spec, id_work_type))
                c.execute('INSERT INTO Orders (ID_Work_Spec, O_Date) values (?,?)',
                          (id_work_spec, str(date.today())))
                c.execute(
                    'SELECT ID FROM Orders WHERE ID_Work_Spec=?', (id_work_spec,))
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
                    'SELECT Cost_m2 FROM C_Services WHERE Naming=?', (values['-S1-'],))
                cost += square * int(c.fetchone()[0])
                window['-COST-'].update(cost)
                conn.commit()
                conn.close()
                if values['-S2-'] and values['-D2-'] and values['-T2-']:
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (ID, W_Date, W_Time) values (?,?,?)',
                              (id_work_spec, values['-D2-'], values['-T2-']))
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
                    window['-COST-'].update(cost)
                    conn.commit()
                    conn.close()
                if values['-S3-'] and values['-D3-'] and values['-T3-']:
                    c = conn.cursor()
                    c.execute('INSERT INTO Work_Spec (ID, W_Date, W_Time) values (?,?,?)',
                              (id_work_spec, values['-D3-'], values['-T3-']))
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
                    window['-COST-'].update(cost)
                    conn.commit()
                    conn.close()
                sg.Popup(
                    f'Заказ создан успешно!\nНомер заказа: {id_order}\nНомер договора: {id_contract}\nСтоимость услуг: {cost}', title='Успешно')
            else:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

    window.close()


def user_give_feedback():
    layout = [
        [sg.Text('Номер заказа:')],
        [sg.InputText(key='-ORDNUM-')],
        [sg.Text(
            'Оцените услуги от 1 до 5, где 1 - очень плохо, 5 - очень хорошо')],
        [sg.Text('Качество работ:'), sg.Combo(
            ['5', '4', '3', '2', '1'], key='-CR1-', default_value='5')],
        [sg.Text('Комментарий:')],
        [sg.Multiline(key='-COMM-', size=(50, 5))],
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
            break

    window.close()


######################################## WORKER ######################################################

# Функция для вывода окна сотрудника
def worker_window():
    layout_worker = [
        [sg.Text('Мои назначения:')],
        [sg.Multiline(key='-ASSIGN-', size=(50, 5))],
        [sg.Push(), sg.Button('Выйти')]
    ]

    window = sg.Window('Клининговая компания. Сотрудник', layout_worker)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Выйти':
            break
    window.close()


sg.theme('sandy beach')  # цветовая тема приложения

# интерфейс главного окна
layout = [
    [sg.Text('Пожалуйста, выполните вход')],
    [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
    [sg.Push(), sg.Text('Пароль:'), sg.InputText(key='-PASS-', password_char='*')],
    [sg.Push(), sg.Button('Войти'), sg.Push()],
    [sg.Push(), sg.Button('Регистрация физ. лица'),
     sg.Button('Регистрация юр. лица'), sg.Push()],
    [sg.Push(), sg.Button('Выход')]
]

window = sg.Window('Клининговая компания. Вход',
                   layout)  # открытие главного окна

while True:
    event, values = window.read()  # отслеживание состояния и переменных главного окна

    # обработка события выхода из приложения
    if event == sg.WINDOW_CLOSED or event == 'Выход':
        break

    # обработка события нажатия на кнопку "Регистрация физ. лица"
    if event == 'Регистрация физ. лица':
        register_ind()

    # обработка события нажатия на кнопку "Регистрация юр. лица"
    if event == 'Регистрация юр. лица':
        register_ent()

    # обработка события нажатия на кнопку "Войти"
    if event == 'Войти':

        # запуск окна админа (проверка логина и пароля admin)
        if values['-LOGIN-'] == 'admin' and values['-PASS-'] == 'admin':
            window_admin = admin_window()
            while True:
                event_a, values_a = window_admin.read()
                if event_a == sg.WINDOW_CLOSED or event_a == 'Выйти':
                    break
                if event_a == 'Добавить услугу':
                    admin_add_service()
                if event_a == 'Добавить тип работ':
                    admin_add_work_type()
                if event_a == 'Добавить должность':
                    admin_add_position()
                if event_a == 'Добавить сотрудника':
                    admin_add_worker()
                if event_a == 'Просмотреть клиентов':
                    admin_list_clients()
                if event_a == 'Просмотреть сотрудников':
                    admin_list_workers()
                if event_a == 'Просмотреть договоры':
                    admin_list_contracts()
                if event_a == 'Просмотреть заказы':
                    admin_list_orders()
                if event_a == 'Назначить сотрудника':
                    admin_assign_worker()
            window_admin.close()

        elif udb.dexists(values['-LOGIN-']) and udb.get(values['-LOGIN-'])[0] == values['-PASS-'] and udb.get(values['-LOGIN-'])[-1] == 'ind':
            window_user = user_window()
            while True:
                event_u, values_u = window_user.read()
                if event_u == sg.WINDOW_CLOSED or event_u == 'Закрыть':
                    break
                if event_u == 'Создать заявку':
                    user_create_order_ind(values['-LOGIN-'])
                if event_u == 'Просмотреть мои заявки':
                    pass
                if event_u == 'Оставить отзыв':
                    user_give_feedback()
            window_user.close()

        elif udb.dexists(values['-LOGIN-']) and udb.get(values['-LOGIN-'])[0] == values['-PASS-'] and udb.get(values['-LOGIN-'])[-1] == 'ent':
            window_user = user_window()
            while True:
                event_u, values_u = window_user.read()
                if event_u == sg.WINDOW_CLOSED or event_u == 'Закрыть':
                    break
                if event_u == 'Создать заявку':
                    user_create_order_ent(values['-LOGIN-'])
                if event_u == 'Просмотреть мои заявки':
                    pass
                if event_u == 'Оставить отзыв':
                    user_give_feedback()
            window_user.close()

        elif udb.dexists(values['-LOGIN-']) and udb.get(values['-LOGIN-'])[0] == values['-PASS-'] and udb.get(values['-LOGIN-'])[-1] == 'wrk':
            worker_window()

        # обработка ошибки ввода неизвестного логина и пароля
        else:
            sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

window.close()  # закрытие главного окна
