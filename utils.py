import PySimpleGUI as sg
import sqlite3
import pickledb
from tinydb import TinyDB, Query

rdb = pickledb.load('rates.db', False)
udb = pickledb.load('users.db', False)
ord_db = TinyDB('orders.db')


# Каскадное обновление серии и номера паспорта сотрудника
def worker_cascade_update_psn(old_psn, new_psn):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('UPDATE Employees SET Passport_SN=? WHERE Passport_SN=?',
              (new_psn, old_psn))
    c.execute('UPDATE Employees_Individuals SET Passport_SN_Employees=? WHERE Passport_SN_Employees=?', (new_psn, old_psn))
    c.execute('UPDATE Employees_Entities SET Passport_SN_Employees=? WHERE Passport_SN_Employees=?', (new_psn, old_psn))
    conn.commit()
    conn.close()


# Каскадное обновление должности и зарплаты сотрудника
def worker_cascade_update_pos(psn, new_pos):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('UPDATE Employees SET ID_Positions=? WHERE Passport_SN=?',
              (new_pos, psn))
    c.execute('SELECT Salary FROM Positions WHERE ID=?', (new_pos,))
    sal = c.fetchone()[0]
    c.execute('UPDATE Employees SET Salary=? WHERE Passport_SN=?', (sal, psn))
    conn.commit()
    conn.close()


# Каскадное удаление сотрудника
def worker_cascade_delete(psn):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('DELETE FROM Employees WHERE Passport_SN=?', (psn,))
    c.execute(
        'DELETE FROM Employees_Individuals WHERE Passport_SN_Employees=?', (psn,))
    c.execute('DELETE FROM Employees_Entities WHERE Passport_SN_Employees=?', (psn,))
    udb.rem(str(psn))
    udb.dump()
    conn.commit()
    conn.close()


# Вспомогательная функция для назначения должности сотруднику, чья прошлая должность была удалена
def position_delete_helper(id_pos):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('SELECT Naming FROM Positions WHERE ID<>?', (id_pos,))
    combo = []
    for pos in c.fetchall():
        combo.append(pos[0])
    combo2 = []
    c.execute('SELECT Passport_SN FROM Employees WHERE ID_Positions=?', (id_pos,))
    for pos in c.fetchall():
        combo2.append(pos[0])
    res_emps = 'Паспорт Фамилия Имя Отчество Должность Зарплата Дата рождения Дата выхода на работу\n\n'
    c.execute('SELECT * FROM Employees WHERE ID_Positions=?', (id_pos,))
    emps = c.fetchall()
    for emp in emps:
        id_pos = emp[1]
        c.execute('SELECT Naming FROM Positions WHERE ID=?', (id_pos,))
        pos_name = c.fetchone()[0]
        res_emps += f'{emp[0]} {emp[4]} {emp[2]} {emp[3]} {pos_name} {emp[5]} р. {emp[6]} {emp[7]}\n'
    conn.close()

    layout = [
        [sg.Text('Назначьте новые должности следующим сотрудникам:')],
        [sg.Multiline(key='-EMPS-', size=(50, 5), default_text=res_emps)],
        [sg.Text('Сотрудник:')],
        [sg.Combo(combo2, key='-EMP-')],
        [sg.Text('Новая должность:')],
        [sg.Combo(combo, key='-POS-')],
        [sg.Button('Назначить'), sg.Button('Не сейчас')]
    ]

    window = sg.Window('Назначить новые должности', layout)
    while True:
        event, values = window.read()
        if event == 'Не сейчас' or event == sg.WINDOW_CLOSED:
            conn = sqlite3.connect('Cleaning_Company.db')
            c = conn.cursor()
            c.execute('SELECT ID FROM Positions WHERE Naming=?',
                      ('<Не назначено>',))
            id_none = c.fetchone()[0]
            c.execute(
                'UPDATE Employees SET ID_Positions=?, Salary=? WHERE Passport_SN=?', (id_none, 0, id_pos))
            c.execute('DELETE FROM Positions WHERE ID=?', (id_pos,))
            conn.commit()
            conn.close()
            break

        if event == 'Назначить':
            conn = sqlite3.connect('Cleaning_Company.db')
            c = conn.cursor()
            c.execute('SELECT * FROM Positions WHERE Naming=?',
                      (values['-POS-'],))
            new_id = c.fetchone()[1]
            new_sal = c.fetchone()[2]
            c.execute('UPDATE Employees SET ID_Positions=?, Salary=? WHERE Passport_SN=?',
                      (new_id, new_sal, values['-EMP-']))
            conn.commit()
            conn.close()
            res_emps = 'Паспорт Фамилия Имя Отчество Должность Зарплата Дата рождения Дата выхода на работу\n\n'
            c.execute('SELECT * FROM Employees WHERE ID_Positions=?', (id_pos,))
            emps = c.fetchall()
            if emps == []:
                conn = sqlite3.connect('Cleaning_Company.db')
                c = conn.cursor()
                c.execute('DELETE FROM Positions WHERE ID=?', (id_pos,))
                conn.commit()
                conn.close()
                break
            else:
                for emp in emps:
                    id_pos = emp[1]
                    c.execute(
                        'SELECT Naming FROM Positions WHERE ID=?', (id_pos,))
                    pos_name = c.fetchone()[0]
                    res_emps += f'{emp[0]} {emp[4]} {emp[2]} {emp[3]} {pos_name} {emp[5]} р. {emp[6]} {emp[7]}\n'
                window['-EMPS-'].update(res_emps)

    window.close()
