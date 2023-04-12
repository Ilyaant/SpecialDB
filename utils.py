import PySimpleGUI as sg
import sqlite3
import pickledb
from tinydb import TinyDB, Query

rdb = pickledb.load('rates.db', False)
udb = pickledb.load('users.db', False)
ord_db = TinyDB('orders.db')


def worker_cascade_update_psn(old_psn, new_psn):
    conn = sqlite3.connect('Cleaning_Company.db')
    c = conn.cursor()
    c.execute('UPDATE Employees SET Passport_SN=? WHERE Passport_SN=?',
              (new_psn, old_psn))
    c.execute('UPDATE Employees_Individuals SET Passport_SN_Employees=? WHERE Passport_SN_Employees=?', (new_psn, old_psn))
    c.execute('UPDATE Employees_Entities SET Passport_SN_Employees=? WHERE Passport_SN_Employees=?', (new_psn, old_psn))
    conn.commit()
    conn.close()


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
