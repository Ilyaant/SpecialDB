import PySimpleGUI as sg


def admin_window():
    layout_admin = [
        [sg.Text('Admin')]
    ]
    return sg.Window('Клининговая компания. Администратор', layout_admin)


def user_window():
    layout_user = [
        [sg.Text('User')]
    ]
    return sg.Window('Клининговая компания. Пользователь', layout_user)


def worker_window():
    layout_worker = [
        [sg.Text('Worker')]
    ]
    return sg.Window('Клининговая компания. Пользователь', layout_worker)


sg.theme('sandy beach')

layout = [
    [sg.Text('Пожалуйста, выполните вход')],
    [sg.Text('Логин:'), sg.InputText(key='-LOGIN-')],
    [sg.Text('Пароль:'), sg.InputText(key='-PASS-')],
    [sg.Button('Войти'), sg.Push(), sg.Button('Выход')]
]

window = sg.Window('Клининговая компания. Вход', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Выход':
        break

    if event == 'Войти':
        if values['-LOGIN-'] == 'admin' and values['-PASS-'] == 'admin':
            window_admin = admin_window()
            while True:
                event_a, values_a = window_admin.read()
                if event_a == sg.WINDOW_CLOSED:
                    break
            window_admin.close()

        elif values['-LOGIN-'] == 'user' and values['-PASS-'] == 'user':
            window_user = user_window()
            while True:
                event_u, values_u = window_user.read()
                if event_u == sg.WINDOW_CLOSED:
                    break
            window_user.close()

        elif values['-LOGIN-'] == 'worker' and values['-PASS-'] == 'worker':
            window_worker = worker_window()
            while True:
                event_w, values_w = window_worker.read()
                if event_w == sg.WINDOW_CLOSED:
                    break
            window_worker.close()

        else:
            sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

window.close()
