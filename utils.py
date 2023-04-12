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
