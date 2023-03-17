import PySimpleGUI as sg
import sqlite3


# Функция для вывода окна админа
def admin_window():
    layout_admin = [
        [sg.Button('Добавить услугу'), sg.Button('Добавить тип работ')],
        [sg.Button('Добавить должность'), sg.Button('Добавить сотрудника')],
        [sg.Button('Просмотреть клиентов'),
         sg.Button('Просмотреть сотрудников')],
        [sg.Button('Просмотреть договоры'), sg.Button('Просмотреть заказы')],
        [sg.Push(), sg.Button('Закрыть')]
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
                                                         close_when_date_chosen=True, target='-WBDATE-', format='%Y:%m:%d')],
        [sg.Text('Дата приема на работу:')],
        [sg.InputText(key='-WHDATE-'), sg.CalendarButton('Выбрать дату',
                                                         close_when_date_chosen=True, target='-WHDATE-', format='%Y:%m:%d')],
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
                break
    window.close()


# Функция для вывода окна пользователя
def user_window():
    layout_user = [
        [sg.Text('User')]
    ]
    return sg.Window('Клининговая компания. Пользователь', layout_user)


# Функция для вывода окна сотрудника
def worker_window():
    layout_worker = [
        [sg.Text('Worker')]
    ]
    return sg.Window('Клининговая компания. Пользователь', layout_worker)


sg.theme('sandy beach')  # цветовая тема приложения

# интерфейс главного окна
layout = [
    [sg.Text('Пожалуйста, выполните вход')],
    [sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
    [sg.Text('Пароль:'), sg.InputText(key='-PASS-', password_char='*')],
    [sg.Button('Войти'), sg.Push(), sg.Button('Выход')]
]

window = sg.Window('Клининговая компания. Вход',
                   layout)  # открытие главного окна

while True:
    event, values = window.read()  # отслеживание состояния и переменных главного окна

    # обработка события выхода из приложения
    if event == sg.WINDOW_CLOSED or event == 'Выход':
        break

    # обработка события нажатия на кнопку "Войти"
    if event == 'Войти':

        # запуск окна админа (проверка логина и пароля admin)
        if values['-LOGIN-'] == 'admin' and values['-PASS-'] == 'admin':
            window_admin = admin_window()
            while True:
                event_a, values_a = window_admin.read()
                if event_a == sg.WINDOW_CLOSED or event_a == 'Закрыть':
                    break
                if event_a == 'Добавить услугу':
                    admin_add_service()
                if event_a == 'Добавить тип работ':
                    admin_add_work_type()
                if event_a == 'Добавить должность':
                    admin_add_position()
                if event_a == 'Добавить сотрудника':
                    admin_add_worker()
            window_admin.close()

        # запуск окна пользователя (проверка логина и пароля user)
        elif values['-LOGIN-'] == 'user' and values['-PASS-'] == 'user':
            window_user = user_window()
            while True:
                event_u, values_u = window_user.read()
                if event_u == sg.WINDOW_CLOSED:
                    break
            window_user.close()

        # запуск окна работника (проверка логина и пароля worker)
        elif values['-LOGIN-'] == 'worker' and values['-PASS-'] == 'worker':
            window_worker = worker_window()
            while True:
                event_w, values_w = window_worker.read()
                if event_w == sg.WINDOW_CLOSED:
                    break
            window_worker.close()

        # обработка ошибки ввода неизвестного логина и пароля
        else:
            sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

window.close()  # закрытие главного окна
