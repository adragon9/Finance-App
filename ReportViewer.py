import sqlite3

from AppData import Window


def db_get_expenses():
    connection = sqlite3.Connection('Users.db')
    cursor = connection.cursor()
    # print(Window.saved_dat_user)
    if Window.month_sel is None or Window.year_sel is None:
        cursor.execute("""
        SELECT category_name, expense_amount
        FROM expenses
        WHERE user_name = ?
        AND strftime('%m-%Y', expense_added) = strftime('%m-%Y', 'now')
        ORDER BY category_name ASC""", (Window.saved_dat_user,))
    else:
        user_date = f"{Window.month_sel}-{Window.year_sel}"
        cursor.execute("""
        SELECT category_name, expense_amount
        FROM expenses
        WHERE user_name = ?
        AND strftime('%m-%Y', expense_added) = ?
        ORDER BY category_name ASC""", (Window.saved_dat_user, user_date))

    dat = cursor.fetchall()
    print(dat)
    return dat
