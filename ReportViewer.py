import sqlite3


def db_get_all():
    connection = sqlite3.Connection('Users.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM users""")
    dat = cursor.fetchall()

    return dat


def db_get_expense_total(user):
    connection = sqlite3.Connection('Users.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT category_name, expense_amount FROM expenses WHERE user_name = ?""", (user,))
    dat = cursor.fetchall()

    # print(dat)
    return dat
