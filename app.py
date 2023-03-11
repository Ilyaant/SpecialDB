import PySimpleGUI as sg


# Функция для вывода окна админа
def admin_window():
    layout_admin = [
        [sg.Text('Admin')]
    ]
    return sg.Window('Клининговая компания. Администратор', layout_admin)


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
    [sg.Text('Пароль:'), sg.InputText(key='-PASS-')],
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
                if event_a == sg.WINDOW_CLOSED:
                    break
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
