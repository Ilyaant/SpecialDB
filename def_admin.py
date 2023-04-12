import PySimpleGUI as sg
import sqlite3
import pickledb
from tinydb import TinyDB, Query
from utils import *

rdb = pickledb.load('rates.db', False)
udb = pickledb.load('users.db', False)
ord_db = TinyDB('orders.db')


# Функция для вывода окна админа
def admin_window():
    layout_admin = [
        [sg.Button('Добавить услугу'), sg.Push(),
         sg.Button('Просмотреть клиентов')],
        [sg.Button('Добавить должность'), sg.Push(),
         sg.Button('Просмотреть сотрудников')],
        [sg.Button('Добавить сотрудника'), sg.Push(),
         sg.Button('Просмотреть услуги')],
        [sg.Button('Назначить сотрудника'), sg.Push(),
         sg.Button('Просмотреть заказы')],
        [sg.Push()],
        [sg.Button('Редактировать сотрудника'),
         sg.Button('Удалить сотрудника', button_color='red')],
        [sg.Push(), sg.Button('Выйти')]
    ]
    return sg.Window('Клининговая компания. Администратор', layout_admin)


# Функция для добавления новой услуги
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


# Функция для добавления нового типа работ
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


# Функция для добавления новой должности
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


# Функция для добавления нового работника
def admin_add_worker():
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('SELECT Naming FROM Positions')
    combo = []
    for pos in c.fetchall():
        combo.append(pos[0])
    conn.close()

    layout = [
        [sg.Text('Серия и номер паспорта:')],
        [sg.InputText(key='-WSN-')],
        [sg.Text('Должность:')],
        [sg.Combo(combo, key='-WPOS-')],
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
                c.execute("SELECT * FROM Positions WHERE Naming=?",
                          (values['-WPOS-'],))
                id_pos = c.fetchone()[0]
                worker = (int(values['-WSN-']), id_pos, values['-WFNAME-'],
                          values['-WSNAME-'], values['-WLNAME-'], values['-WBDATE-'], values['-WHDATE-'])
                conn.close()
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute('SELECT Salary FROM Positions WHERE ID=?', (id_pos,))
                sal = int(c.fetchone()[0])
                worker = (int(values['-WSN-']), id_pos, values['-WFNAME-'],
                          values['-WSNAME-'], values['-WLNAME-'], sal, values['-WBDATE-'], values['-WHDATE-'])
                c.execute(
                    'INSERT INTO Employees (Passport_SN, ID_Positions, F_Name, S_Name, L_Name, Salary, Date_Birth, Date_hire) VALUES (?,?,?,?,?,?,?,?)', worker)
                conn.commit()
                conn.close()
                udb.set(values['-WSN-'], [values['-WLNAME-'], 'wrk'])
                udb.dump()
                break
    window.close()


# Функция для редактирования работника
def admin_edit_worker():
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('SELECT Passport_SN FROM Employees')
    combo = []
    for emp in c.fetchall():
        combo.append(emp[0])

    c.execute('SELECT Naming FROM Positions')
    combo2 = []
    for pos in c.fetchall():
        combo2.append(pos[0])
    conn.close()

    psn = None
    pos = None

    layout = [
        [sg.Text('Выберите сотрудника для редактирования:')],
        [sg.Combo(combo, key='-WRK-', enable_events=True)],
        [sg.Text('Серия и номер паспорта:')],
        [sg.InputText(key='-WSN-')],
        [sg.Text('Должность:')],
        [sg.Combo(combo2, key='-WPOS-')],
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
        [sg.Button('Внести изменения'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Редактировать сотрудника', layout)
    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == '-WRK-':
            psn = int(values['-WRK-'])
            conn = sqlite3.connect('Cleaning_Company.db')
            c = conn.cursor()
            c.execute('SELECT * FROM Employees WHERE Passport_SN=?', (psn,))
            wrk = c.fetchone()
            c.execute('SELECT Naming FROM Positions WHERE ID=?',
                      (int(wrk[1]),))
            pos = c.fetchone()[0]
            window['-WSN-'].update(wrk[0])
            window['-WPOS-'].update(pos)
            window['-WFNAME-'].update(wrk[2])
            window['-WSNAME-'].update(wrk[3])
            window['-WLNAME-'].update(wrk[4])
            window['-WBDATE-'].update(wrk[6])
            window['-WHDATE-'].update(wrk[7])
            conn.close()

        if event == 'Внести изменения':
            conn = sqlite3.connect('Cleaning_Company.db')
            c = conn.cursor()
            c.execute('SELECT ID FROM Positions WHERE Naming=?',
                      (values['-WPOS-'],))
            new_pos_id = int(c.fetchone()[0])
            new_wrk = (
                values['-WFNAME-'],
                values['-WSNAME-'],
                values['-WLNAME-'],
                values['-WBDATE-'],
                values['-WHDATE-'],
                psn
            )
            conn.close()
            if psn != int(values['-WSN-']) and pos != values['-WPOS-']:
                worker_cascade_update_pos(psn, new_pos_id)
                worker_cascade_update_psn(psn, int(values['-WSN-']))
                new_wrk = (
                    values['-WFNAME-'],
                    values['-WSNAME-'],
                    values['-WLNAME-'],
                    values['-WBDATE-'],
                    values['-WHDATE-'],
                    int(values['-WSN-'])
                )
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'UPDATE Employees SET F_Name=?, S_Name=?, L_Name=?, Date_Birth=?, Date_hire=? WHERE Passport_SN=?', new_wrk)
                conn.commit()
                conn.close()
                udb.rem(str(psn))
                udb.set(values['-WSN-'], [values['-WLNAME-'], 'wrk'])
                udb.dump()
                sg.Popup('Успешно', title='Успешно')
            elif psn != int(values['-WSN-']):
                worker_cascade_update_psn(psn, int(values['-WSN-']))
                new_wrk = (
                    values['-WFNAME-'],
                    values['-WSNAME-'],
                    values['-WLNAME-'],
                    values['-WBDATE-'],
                    values['-WHDATE-'],
                    int(values['-WSN-'])
                )
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'UPDATE Employees SET F_Name=?, S_Name=?, L_Name=?, Date_Birth=?, Date_hire=? WHERE Passport_SN=?', new_wrk)
                conn.commit()
                conn.close()
                udb.rem(str(psn))
                udb.set(values['-WSN-'], [values['-WLNAME-'], 'wrk'])
                udb.dump()
                sg.Popup('Успешно', title='Успешно')
            elif pos != values['-WPOS-']:
                worker_cascade_update_pos(psn, new_pos_id)
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'UPDATE Employees SET F_Name=?, S_Name=?, L_Name=?, Date_Birth=?, Date_hire=? WHERE Passport_SN=?', new_wrk)
                udb.rem(values['-WSN-'])
                udb.set(values['-WSN-'], [values['-WLNAME-'], 'wrk'])
                udb.dump()
                conn.commit()
                conn.close()
                sg.Popup('Успешно', title='Успешно')
            else:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute(
                    'UPDATE Employees SET F_Name=?, S_Name=?, L_Name=?, Date_Birth=?, Date_hire=? WHERE Passport_SN=?', new_wrk)
                udb.rem(values['-WSN-'])
                udb.set(values['-WSN-'], [values['-WLNAME-'], 'wrk'])
                udb.dump()
                conn.commit()
                conn.close()
                sg.Popup('Успешно', title='Успешно')

    window.close()


# Функция для просмотра всех клиентов
def admin_list_clients():
    layout = [
        [sg.Text('Физические лица:')],
        [sg.Multiline(key='-IND-', size=(50, 5))],
        [sg.Text('Юридические лица:')],
        [sg.Multiline(key='-ENT-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть клиентов', layout, finalize=True)

    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    res_inds = 'Паспорт Фамилия Имя Отчество Адрес Площадь\n\n'
    c.execute('SELECT * FROM Individuals')
    inds = c.fetchall()
    for ind in inds:
        res_inds += f'{ind[0]} {ind[3]} {ind[2]} {ind[1]} {ind[4]}, {ind[5]} кв. м\n'
    window['-IND-'].update(res_inds)
    res_ents = 'Название Адрес Площадь\n\n'
    c.execute('SELECT * FROM Entities')
    ents = c.fetchall()
    for ent in ents:
        res_ents += f'{ent[1]} {ent[3]}, {ent[2]} кв. м\n'
    window['-ENT-'].update(res_ents)
    conn.close()

    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break

    window.close()


# Функция для просмотра всех работников
def admin_list_workers():
    layout = [
        [sg.Text('Сотрудники:')],
        [sg.Multiline(key='-EMP-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть сотрудников', layout, finalize=True)

    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    res_emps = 'Паспорт Фамилия Имя Отчество Должность Зарплата Дата рождения Дата выхода на работу\n\n'
    c.execute('SELECT * FROM Employees')
    emps = c.fetchall()
    for emp in emps:
        id_pos = emp[1]
        c.execute('SELECT Naming FROM Positions WHERE ID=?', (id_pos,))
        pos_name = c.fetchone()[0]
        c.execute('SELECT Salary FROM Positions WHERE ID=?', (id_pos,))
        sal = int(c.fetchone()[0])
        res_emps += f'{emp[0]} {emp[4]} {emp[2]} {emp[3]} {pos_name} {sal} р. {emp[6]} {emp[7]}\n'
    window['-EMP-'].update(res_emps)
    conn.close()

    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break

    window.close()


# Функция для просмотра всех договоров
def admin_list_contracts():
    layout = [
        [sg.Text('Договоры c юридическими лицами:')],
        [sg.Multiline(key='-CON_ENT-', size=(50, 5))],
        [sg.Text('Договоры c физическими лицами:')],
        [sg.Multiline(key='-CON_IND-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть договоры', layout, finalize=True)

    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    res_contr_ent = 'Номер Название компании Название договора Дата подписания Номер заказа\n\n'
    c.execute('SELECT * FROM Contracts')
    contrs_ent = c.fetchall()
    for contr in contrs_ent:
        res_contr_ent += f'{contr[0]} {contr[1]} {contr[2]} {contr[3]} {contr[4]}\n'
    window['-CON_ENT-'].update(res_contr_ent)
    res_contr_ind = 'Номер Паспорт Название договора Дата подписания Номер заказа\n\n'
    c.execute('SELECT * FROM Contracts')
    contrs_ind = c.fetchall()
    for c in contrs_ind:
        res_contr_ind += f'{c[0]} {c[1]} {c[2]} {c[3]} {c[4]}\n'
    window['-CON_IND-'].update(res_contr_ind)
    conn.close()

    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break

    window.close()


# Функция для просмотра всех заказов
def admin_list_orders():
    layout = [
        [sg.Text('Заказы юридических лиц:')],
        [sg.Multiline(key='-ORD_ENT-', size=(50, 5))],
        [sg.Text('Заказы физических лиц:')],
        [sg.Multiline(key='-ORD_IND-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотреть заказы', layout, finalize=True)

    res_ent = ''
    res_ind = ''
    search = ord_db.all()
    for s in search:
        login = s['login']
        if udb.get(login)[-1] == 'ent':
            res_ent += f'Заказ {s["num"]} от {udb.get(login)[1]}\nУслуга 1: {s["S1"]}, {s["D1"]}, {s["T1"]}\n'
            if s['S2'] != '':
                res_ent += f'Услуга 2: {s["S2"]}, {s["D2"]}, {s["T2"]}\n'
                if s['S3'] != '':
                    res_ent += f'Услуга 3: {s["S3"]}, {s["D3"]}, {s["T3"]}\n'
            res_ent += '\n'
        if udb.get(login)[-1] == 'ind':
            res_ind += f'Заказ {s["num"]}\nУслуга 1: {s["S1"]}, {s["D1"]}, {s["T1"]}\n'
            if s['S2'] != '':
                res_ind += f'Услуга 2: {s["S2"]}, {s["D2"]}, {s["T2"]}\n'
                if s['S3'] != '':
                    res_ind += f'Услуга 3: {s["S3"]}, {s["D3"]}, {s["T3"]}\n'
            res_ind += '\n'

    window['-ORD_ENT-'].update(res_ent)
    window['-ORD_IND-'].update(res_ind)

    while True:
        event, values = window.read()
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break

    window.close()


# Функция для просмотра услуг
def admin_list_services():
    layout = [
        [sg.Text('Доступные услуги:')],
        [sg.Multiline(key='-SERV-', size=(50, 5))],
        [sg.Push(), sg.Button('Закрыть')]
    ]

    window = sg.Window('Просмотр услуг', layout, finalize=True)

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
        if event == 'Закрыть' or event == sg.WINDOW_CLOSED:
            break

    window.close()


# Функция для назначения работника на заказ
def admin_assign_worker():
    combo = []
    User = Query()
    search = ord_db.search(User.status == 'not completed')
    for s in search:
        combo.append(s['num'])

    combo2 = []
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('SELECT Passport_SN FROM Employees')
    for w in c.fetchall():
        combo2.append(w[0])
    conn.close()

    layout = [
        [sg.Text('Список заказов:')],
        [sg.Multiline(key='-ORD-', size=(50, 5))],
        [sg.Text('Номер заказа:'), sg.Combo(combo, key='-ORDNUM-')],
        [sg.Text('Серия и номер паспорта сотрудника:'),
         sg.Combo(combo2, key='-WRK-')],
        [sg.Button('Назначить'), sg.Push(), sg.Button('Отмена')]
    ]

    window = sg.Window('Назначить сотрудника', layout, finalize=True)

    res = ''
    User = Query()
    search = ord_db.search(User.status == 'not completed')
    for s in search:
        res += f'Заказ {s["num"]}\nУслуга 1: {s["S1"]}, {s["D1"]}, {s["T1"]}\n'
        if s['S2'] != '':
            res += f'Услуга 2: {s["S2"]}, {s["D2"]}, {s["T2"]}\n'
            if s['S3'] != '':
                res += f'Услуга 3: {s["S3"]}, {s["D3"]}, {s["T3"]}\n'
        res += '\n'
    window['-ORD-'].update(res)

    while True:
        event, values = window.read()
        if event == 'Отмена' or event == sg.WINDOW_CLOSED:
            break

        if event == 'Назначить':
            try:
                num = int(values['-ORDNUM-'])
                psn = int(values['-WRK-'])
            except:
                sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
            else:
                User = Query()
                login = ord_db.search(User.num == num)[0]['login']
                id_user = udb.get(login)[1]
                type_user = udb.get(login)[-1]
                if type_user == 'ind':
                    conn = sqlite3.connect('Cleaning_Company.db')
                    c = conn.cursor()
                    c.execute(
                        'INSERT INTO Employees_Individuals (Passport_SN_Employees, Passport_SN_Individuals) VALUES (?, ?)', (psn, int(id_user)))
                    conn.commit()
                    conn.close()
                    sg.Popup('Работник назначен успешно', title='Успешно')
                if type_user == 'ent':
                    conn = sqlite3.connect('Cleaning_Company.db')
                    c = conn.cursor()
                    c.execute(
                        'SELECT ID FROM Entities WHERE Naming=?', (str(id_user),))
                    id_ent = int(c.fetchone()[0])
                    c.execute(
                        'INSERT INTO Employees_Entities (Passport_SN_Employees, ID_Entities) VALUES (?, ?)', (psn, id_ent))
                    conn.commit()
                    conn.close()
                    sg.Popup('Работник назначен успешно', title='Успешно')

                User = Query()
                ord_db.update({'status': 'assigned'}, User.num == num)
                res = ''
                User = Query()
                search = ord_db.search(User.status == 'not completed')
                for s in search:
                    res += f'Заказ {s["num"]}\nУслуга 1: {s["S1"]}, {s["D1"]}, {s["T1"]}\nУслуга 2: {s["S2"]}, {s["D2"]}, {s["T2"]}\nУслуга 3: {s["S3"]}, {s["D3"]}, {s["T3"]}\n\n'
                res = res
                window['-ORD-'].update(res)
    window.close()
