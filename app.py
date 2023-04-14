import PySimpleGUI as sg

from utils import *
from def_admin import *
from def_user import *
from def_worker import *

sg.theme('sandy beach')  # цветовая тема приложения


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
        [sg.Button('Редактировать должность'),
         sg.Button('Удалить должность', button_color='red')],
        [sg.Push(), sg.Button('Выйти')]
    ]
    return sg.Window('Клининговая компания. Администратор', layout_admin)


# интерфейс главного окна
layout = [
    [sg.Text('Пожалуйста, выполните вход')],
    [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-', do_not_clear=False)],
    [sg.Push(), sg.Text('Пароль:'), sg.InputText(
        key='-PASS-', password_char='*', do_not_clear=False)],
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
                if event_a == 'Просмотреть услуги':
                    admin_list_services()
                if event_a == 'Редактировать сотрудника':
                    admin_edit_worker()
                if event_a == 'Удалить сотрудника':
                    admin_delete_worker()
                if event_a == 'Редактировать должность':
                    admin_edit_position()
                if event_a == 'Удалить должность':
                    admin_delete_position()
            window_admin.close()

        # запуск окна пользователя (физ. лица)
        elif udb.get(values['-LOGIN-']) and udb.get(values['-LOGIN-'])[0] == values['-PASS-'] and udb.get(values['-LOGIN-'])[-1] == 'ind':
            window_user = user_window()
            while True:
                event_u, values_u = window_user.read()
                if event_u == sg.WINDOW_CLOSED or event_u == 'Закрыть':
                    break
                if event_u == 'Создать заявку':
                    user_create_order_ind(values['-LOGIN-'])
                if event_u == 'Просмотреть мои заказы':
                    user_list_orders(values['-LOGIN-'])
                if event_u == 'Оставить отзыв':
                    user_give_feedback()
            window_user.close()

        # запуск окна пользователя (юр. лица)
        elif udb.get(values['-LOGIN-']) and udb.get(values['-LOGIN-'])[0] == values['-PASS-'] and udb.get(values['-LOGIN-'])[-1] == 'ent':
            window_user = user_window()
            while True:
                event_u, values_u = window_user.read()
                if event_u == sg.WINDOW_CLOSED or event_u == 'Закрыть':
                    break
                if event_u == 'Создать заявку':
                    user_create_order_ent(values['-LOGIN-'])
                if event_u == 'Просмотреть мои заказы':
                    user_list_orders(values['-LOGIN-'])
                if event_u == 'Оставить отзыв':
                    user_give_feedback()
            window_user.close()

        # запуск окна работника
        elif udb.get(values['-LOGIN-']) and udb.get(values['-LOGIN-'])[0] == values['-PASS-'] and udb.get(values['-LOGIN-'])[-1] == 'wrk':
            worker_window(int(values['-LOGIN-']))

        # обработка ошибки ввода неизвестного логина и пароля
        else:
            sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')

window.close()  # закрытие главного окна
