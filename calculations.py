import datetime
import sqlite3
from time import strftime

from AppData import Window


def total_expenses():
    connection = sqlite3.Connection('Users.db')
    cursor = connection.cursor()
    # Debug
    # print(Window.month_sel)
    if Window.month_sel is None or Window.year_sel is None:
        cursor.execute("""
        SELECT expense_amount
        FROM expenses
        WHERE user_name = ?
        AND strftime('%m-%Y', expense_added) = strftime('%m-%Y', 'now')""", (Window.saved_dat_user,))
    else:
        user_date = f"{Window.month_sel}-{Window.year_sel}"
        cursor.execute("""
        SELECT expense_amount
        FROM expenses
        WHERE user_name = ?
        AND strftime('%m-%Y', expense_added) = ?""", (Window.saved_dat_user, user_date))

    expenses = cursor.fetchall()
    Window.calc_total_expenses = 0
    for expense in expenses:
        Window.calc_total_expenses += float(expense[0])

    return f"Your total expenses amount to: ${Window.calc_total_expenses:,.2f} for this month."


def net_income():
    current_date = datetime.datetime.now().strftime('%m-%Y')
    user_date = f"{Window.month_sel}-{Window.year_sel}"

    if Window.calc_total_expenses is None:
        return f"Your net income is: ${Window.current_user.get_income(user_date):,.2f} A PROBLEM OCCURRED TOTAL EXPENSES UNAVAILABLE!"
    else:
        if user_date == current_date:
            Window.calc_monthly_net = Window.saved_dat_income - Window.calc_total_expenses
        else:
            Window.calc_monthly_net = float(Window.current_user.get_income(user_date)) - Window.calc_total_expenses
        net_impact()
        return f"Your net income is: ${Window.calc_monthly_net:,.2f}"


def net_impact():
    # Debug
    # print(Window.saved_dat_balance)
    try:
        Window.calc_balance_impact = Window.calc_monthly_net + Window.saved_dat_balance
    except TypeError:
        Window.calc_balance_impact = None


def cat_breakdown():
    connection = sqlite3.Connection('Users.db')
    cursor = connection.cursor()
    if Window.month_sel is None or Window.year_sel is None:
        cursor.execute("""
        SELECT category_name, expense_amount
        FROM expenses
        WHERE user_name = ?
        AND strftime('%m-%Y', expense_added) = strftime('%m-%Y', 'now')""", (Window.saved_dat_user,))
    else:
        user_date = f"{Window.month_sel}-{Window.year_sel}"
        cursor.execute("""
        SELECT category_name, expense_amount
        FROM expenses
        WHERE user_name = ?
        AND strftime('%m-%Y', expense_added) = ?""", (Window.saved_dat_user, user_date))

    data = cursor.fetchall()
    item_count = {}
    item_value_totals = {}
    item_lists = []
    # Debug
    # print(data)
    for item in data:
        item_count.update({item[0]: 0})
        item_value_totals.update({item[0]: 0})

    for item in data:
        if item[0] in item_count:
            item_count[item[0]] += 1
            item_value_totals[item[0]] += item[1]

    item_lists.append(item_count)
    item_lists.append(item_value_totals)

    return item_lists
