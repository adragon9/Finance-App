import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk

import ReportViewer
import TabManager
import calculations
import user
from AppData import Window
from strings import Strings

with open("config.txt") as strings:
    for line in strings:
        key, value = line.replace(' ', '').strip().split("=")
        if key == "win_width":
            try:
                win_w = int(value)
            except ValueError:
                win_w = 900
        if key == "win_height":
            try:
                win_h = int(value)
            except ValueError:
                win_h = 600


def revert_text(canvas, text):
    canvas.itemconfig(text, text="")


def data_backup():
    connection = sqlite3.connect('Users.db')
    backup_db = sqlite3.connect('Users-backup.db')
    connection.backup(backup_db)
    backup_db.close()
    connection.close()


def get_categories(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute("""
    SELECT category_name 
    FROM expense_categories
    WHERE user_name = ?
    ORDER BY category_name ASC""", (username,))

    fetch = cursor.fetchall()
    categories = []
    for category in fetch:
        categories.append(category[0])
    connection.close()
    return categories

# I think this is a debug function
# def dropdown_control(*args):
    # print(drp_cats.get())


def set_session_balance(balance):
    status = ""
    balance = ''.join(char for char in balance if char.isdigit() or char == '.')
    if balance.strip() == '':
        status = "There is no input for 'balance'!"
        return status
    else:
        try:
            Window.saved_dat_balance = float(balance)
            status = f"Session balance set to: ${Window.saved_dat_balance:,.2f}"
            return status
        except ValueError:
            status = "Your input for 'balance' is not a number!"
            return status


def app_btn_manager(event_id):
    # Needed so that the entire program has access to the current active use.
    # This is due to a lack of foresight as every time this event manager got called the cur_user var got overwritten
    cur_user = user.User(Window.dat_user.get(), Window.dat_password.get())
    # Login button pressed on home tab
    if event_id == 1:
        if cur_user.login():
            # Save the current users data
            Window.current_user = cur_user
            Window.saved_dat_user = Window.dat_user.get()
            Window.saved_dat_pass = Window.dat_password.get()
            Window.saved_dat_income = Window.current_user.get_income()
            Window.dat_dropdown_categories = get_categories(Window.saved_dat_user)
            drp_cats.configure(values=Window.dat_dropdown_categories)
            # Clear the entry boxes
            entry_username.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
            # Disable elements that are unwanted while logged in
            btn_login.configure(state="disabled")
            btn_create_user.configure(state="disabled")
            entry_username.configure(state="disabled")
            entry_pass.configure(state="disabled")
            tabs_canvas[0].itemconfigure(win_login_display, state="hidden")
            tabs_canvas[0].itemconfigure(win_create_user_display, state="hidden")
            tabs_canvas[0].itemconfigure(win_username_display, state="hidden")
            tabs_canvas[0].itemconfigure(win_pass_display, state="hidden")
            tabs_canvas[0].itemconfigure(txt_username, state="hidden")
            tabs_canvas[0].itemconfigure(txt_password, state="hidden")
            tabs_canvas[0].itemconfigure(txt_disclaimer, state="hidden")
            # This enables all the logout buttons
            for k in range(0, num_tabs):
                logouts[k].configure(state='normal')
            # Inform user, update displays, clear inputs
            show_tabs()
            tabs_canvas[0].itemconfig(txt_splash, text=f"Welcome, {cur_user.get_current_user()}")
            tabs_canvas[0].itemconfig(user_info[0], text=Strings.success_login)
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))
        else:
            tabs_canvas[0].itemconfig(user_info[0], text=Strings.fail_login)
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        # Create user event
    # Create user event
    elif event_id == 2:
        status = cur_user.create_user()
        # Debug
        # print(status)
        if status:
            tabs_canvas[0].itemconfig(user_info[0], text=Strings.success_create_user)
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        elif not status and cur_user.get_current_user() is None and cur_user.get_current_password() is None:
            tabs_canvas[0].itemconfig(user_info[0], text=f"{Strings.blank}: BOTH")
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        elif not status and cur_user.get_current_password() is None:
            tabs_canvas[0].itemconfig(user_info[0], text=f"{Strings.blank}: Password")
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        elif not status and cur_user.get_current_user() is None:
            tabs_canvas[0].itemconfig(user_info[0], text=f"{Strings.blank}: USERNAME")
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        elif not status and cur_user.get_current_password() is None:
            tabs_canvas[0].itemconfig(user_info[0], text=f"{Strings.blank}: Password")
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        else:
            tabs_canvas[0].itemconfig(user_info[0], text=Strings.fail_create_user)
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[0], user_info[0]))

        entry_username.delete(0, tk.END)
        entry_pass.delete(0, tk.END)
    # Logout event
    elif event_id == 3:
        # Clear saved user and password
        Window.saved_dat_user = None
        Window.saved_dat_pass = None
        Window.saved_dat_income = None

        # Clear ALL entry boxes on logout
        entry_username.delete(0, tk.END)
        entry_pass.delete(0, tk.END)
        entry_income.delete(0, tk.END)
        entry_expense_amount.delete(0, tk.END)
        entry_expense_cat.delete(0, tk.END)
        entry_expense_desc.delete("1.0", "end-1c")

        # Clear variables
        Window.saved_dat_user = None
        Window.saved_dat_pass = None
        Window.saved_dat_income = None
        Window.saved_dat_balance = None
        Window.saved_dat_expense_cat = None
        Window.saved_dat_expense_desc = None

        # This clears the report display, it has to be activated to edit and then deactivated.
        report_display.config(state="normal")
        report_display.delete("1.0", "end-1c")
        report_display.config(state="disabled")

        # print(Window.saved_dat_user, Window.saved_dat_pass, Window.saved_dat_balance)
        btn_login.configure(state="normal")
        btn_create_user.configure(state="normal")
        entry_username.configure(state="normal")
        entry_pass.configure(state="normal")
        tabs_canvas[0].itemconfigure(win_login_display, state="normal")
        tabs_canvas[0].itemconfigure(win_create_user_display, state="normal")
        tabs_canvas[0].itemconfigure(win_username_display, state="normal")
        tabs_canvas[0].itemconfigure(win_pass_display, state="normal")
        tabs_canvas[0].itemconfigure(txt_username, state="normal")
        tabs_canvas[0].itemconfigure(txt_password, state="normal")
        tabs_canvas[0].itemconfigure(txt_disclaimer, state="normal")
        for k in range(0, num_tabs):
            logouts[k].configure(state='disabled')
        hide_tabs()
        tabs_canvas[0].itemconfig(txt_splash, text=Strings.splash)
    # Submit user balance and income
    elif event_id == 4:
        if Window.current_user is not None:
            data_backup()
            balance = set_session_balance(entry_balance.get())
            income = Window.current_user.set_income(entry_income.get())
            # Update the income
            Window.saved_dat_income = Window.current_user.get_income()
            tabs_canvas[1].itemconfig(user_info[1], text=balance)
            tabs_canvas[1].itemconfig(txt_user_info2, text=income)
            entry_balance.delete(0, tk.END)
            entry_income.delete(0, tk.END)
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[1], user_info[1]))
            root.after(user_info_timer, lambda: revert_text(tabs_canvas[1], txt_user_info2))
        else:
            tabs_canvas[1].itemconfig(user_info[1], text="No user logged in!")
    # Submit new category
    elif event_id == 5:
        Window.saved_dat_expense_desc = entry_expense_desc.get("1.0", "end-1c")
        Window.saved_dat_expense_cat = Window.dat_expense_cat.get()

        entry_expense_desc.delete("1.0", "end-1c")
        entry_expense_cat.delete(0, tk.END)
        # Debug
        # print(Window.saved_dat_expense_cat, Window.saved_dat_expense_desc)
        create_expense = Window.current_user.create_expense_tag(Window.saved_dat_expense_cat, Window.saved_dat_expense_desc)
        # Update the category dropdown box
        Window.dat_dropdown_categories = get_categories(Window.saved_dat_user)
        drp_cats.configure(values=Window.dat_dropdown_categories)

        tabs_canvas[2].itemconfigure(user_info[2], text=create_expense)
        root.after(user_info_timer, lambda: revert_text(tabs_canvas[2], user_info[2]))
    # Add expense of selected type
    elif event_id == 6:
        add_expense = Window.current_user.add_expense(drp_cats.get(), Window.dat_expense_amount.get())
        tabs_canvas[3].itemconfigure(user_info[3], text=add_expense)
        root.after(user_info_timer, lambda: revert_text(tabs_canvas[3], user_info[3]))
        entry_expense_amount.delete(0, tk.END)


def report_event_manager(event_id):
    report_display.config(state="normal")
    report_display.delete("1.0", "end-1c")
    bad_characters = []
    for index, character in enumerate(entry_year.get().strip()):
        if not character.isdigit():
            bad_characters.append(index)

    for index, num in enumerate(bad_characters):
        entry_year.delete(num - index)

    if entry_year.get().strip() == '':
        Window.dat_year.set(datetime.datetime.now().year)

    # First report button
    if event_id == 1:
        # Set the date
        Window.month_sel = drp_months.get()
        Window.year_sel = entry_year.get()
        date = f"{Window.month_sel}-{Window.year_sel}"

        income_report = f"Your saved income is: ${float(Window.current_user.get_income(date)):,.2f}"
        if Window.saved_dat_balance is not None:
            balance_report = f"Your saved balance is: ${float(Window.saved_dat_balance):,.2f}"
        else:
            balance_report = f"You have no saved balance for this session"

        sum_expenses = calculations.total_expenses()
        net_income = calculations.net_income()
        current_time = datetime.datetime.now().strftime("%m-%d-%Y %I:%M:%S %p")
        if Window.calc_balance_impact is not None and abs(Window.calc_monthly_net) > 0:
            impact_report = f"Your balance at the end of the month will go from ${Window.saved_dat_balance:,.2f} to ${Window.calc_balance_impact:,.2f}"
        else:
            impact_report = f"There is no balance impact to report"

        cat_count = calculations.cat_breakdown()[0]
        cat_comparison = calculations.cat_breakdown()[1]

        # Display and format report view
        report_display.insert(tk.END, f"REPORT FOR: {date}\n\n", "center")
        report_display.insert(tk.END, f"GENERATED: {current_time}\n\n", "center")
        report_display.insert(tk.END, sum_expenses, "center")
        report_display.insert(tk.END, '\n' * 2, "center")
        report_display.insert(tk.END, income_report, "center")
        report_display.insert(tk.END, '\n', "center")
        report_display.insert(tk.END, net_income, "center")
        report_display.insert(tk.END, '\n' * 2, "center")
        report_display.insert(tk.END, balance_report, "center")
        report_display.insert(tk.END, '\n', "center")
        report_display.insert(tk.END, impact_report, "center")
        report_display.insert(tk.END, '\n' * 2, "center")
        report_display.insert(tk.END, "--CATEGORY BREAKDOWN--", "center")
        report_display.insert(tk.END, '\n', "center")
        for item, count in cat_count.items():
            report_display.insert(tk.END, f"You had {count} items in the {item}(s) category.", "center")
            report_display.insert(tk.END, '\n', "center")
        # Extra space between lines for visual clarity
        report_display.insert(tk.END, '\n', "center")

        for item, count in cat_comparison.items():
            report_display.insert(tk.END, f"You spent ${count:,.2f} on items in the {item}(s) category.", "center")
            report_display.insert(tk.END, '\n', "center")

    # Lists the expenses of the current user
    elif event_id == 2:
        Window.month_sel = drp_months.get()
        Window.year_sel = entry_year.get()

        rv = ReportViewer.db_get_expenses()
        item_string = ""
        date = f"{Window.month_sel}-{Window.year_sel}"
        report_display.insert(tk.END, f"ALL EXPENSES FOR: {date}\n\n", "center")
        for item in rv:
            for iteration, element in enumerate(item):
                if iteration != len(item) - 1:
                    item_string += f"{element}, "
                else:
                    item_string += f"${element:,.2f};"
            report_display.insert(tk.END, item_string, "center")
            report_display.insert(tk.END, '\n', "center")
            item_string = ""

    report_display.config(state="disabled")


"""
Ensures that all elements stay in relative positions when window size is changed
The event is also a necessary parameter for this function to call correctly as it is needed by .bind()
"""


def window_adjustment(event):
    # Updates items that are always in the same position, the header, logout, etc.
    for t in range(0, num_tabs):
        tabs_w[t] = tabs_canvas[t].winfo_width()
        tabs_h[t] = tabs_canvas[t].winfo_height()
        tabs_canvas[t].coords(headers[t], tabs_w[t] / 2, 0)
        tabs_canvas[t].coords(logouts_windows[t], tabs_w[t] - 20, tabs_h[t] - 10)

    # Needed to reduce flickering on tab change
    root.update_idletasks()
    # Hopefully this will lead to some optimization down the line.
    # Instead of updating all elements it only updates the active tabs elements.
    cur_tab = tabControl.tab(tabControl.select(), "text")
    if cur_tab == tab_names[0]:
        t = 0
        # Readjusts elements to stay in the same position no matter window size
        tabs_canvas[t].coords(txt_splash, tabs_w[t] / 2, tabs_canvas[t].coords(headers[t])[1] + 80)
        tabs_canvas[t].coords(txt_disclaimer, tabs_w[t] * .5, tabs_canvas[t].coords(txt_splash)[1] + 60)
        tabs_canvas[t].coords(win_login_display, tabs_w[t] / 2, tabs_h[t] * .8)
        tabs_canvas[t].coords(win_create_user_display, tabs_w[t] / 2, btn_login.winfo_y() + 45)
        tabs_canvas[t].coords(txt_username, entry_username.winfo_x() - 40, entry_username.winfo_y())
        tabs_canvas[t].coords(win_username_display, tabs_w[t] / 2, tabs_h[t] * .5)
        tabs_canvas[t].coords(txt_password, entry_pass.winfo_x() - 40, entry_pass.winfo_y())
        tabs_canvas[t].coords(win_pass_display, tabs_w[t] / 2, entry_username.winfo_y() + 30)
        tabs_canvas[t].coords(user_info[t], tabs_w[t] / 2, entry_username.winfo_y() + 60)

    elif cur_tab == tab_names[1]:
        t = 1
        tabs_canvas[t].coords(txt_money_disclaimer, tabs_canvas[t].coords(headers[t])[0], tabs_canvas[t].coords(headers[t])[1] + 80)
        tabs_canvas[t].coords(win_balance_display, tabs_w[t] / 2, tabs_h[t] / 2)
        tabs_canvas[t].coords(win_income_display, tabs_canvas[t].coords(win_balance_display)[0], tabs_canvas[t].coords(win_balance_display)[1] + 20)
        tabs_canvas[t].coords(txt_balance_desc, tabs_canvas[t].coords(win_balance_display)[0] - (entry_balance.winfo_reqwidth() / 2) - 35, tabs_canvas[t].coords(win_balance_display)[1])
        tabs_canvas[t].coords(txt_income_desc, tabs_canvas[t].coords(win_income_display)[0] - (entry_income.winfo_reqwidth() / 2) - 35, tabs_canvas[t].coords(win_income_display)[1])
        tabs_canvas[t].coords(win_sbmt_money_display, tabs_canvas[t].coords(win_income_display)[0], tabs_canvas[t].coords(win_income_display)[1] + 45)
        tabs_canvas[t].coords(user_info[t], tabs_canvas[t].coords(win_sbmt_money_display)[0], tabs_canvas[t].coords(win_sbmt_money_display)[1] + 45)
        tabs_canvas[t].coords(txt_user_info2, tabs_canvas[t].coords(user_info[t])[0], tabs_canvas[t].coords(user_info[t])[1] + 20)

    elif cur_tab == tab_names[2]:
        t = 2
        tabs_canvas[t].coords(win_expense_cat, tabs_w[t] / 2, tabs_h[t] / 2)
        tabs_canvas[t].coords(txt_tagger_desc, tabs_canvas[t].coords(headers[t])[0], tabs_canvas[t].coords(headers[t])[1] + 80)
        tabs_canvas[t].coords(win_expense_desc, tabs_w[t] / 2, tabs_canvas[t].coords(win_expense_cat)[1] + 20)
        tabs_canvas[t].coords(win_sbmt_expense, tabs_w[t] / 2, tabs_h[t] - 10)
        tabs_canvas[t].coords(txt_expense_cat, entry_expense_cat.winfo_x() - 10, entry_expense_cat.winfo_y() + 10)
        tabs_canvas[t].coords(txt_expense_desc, tabs_canvas[t].coords(txt_expense_cat)[0], entry_expense_desc.winfo_y() + 10)
        tabs_canvas[t].coords(user_info[t], tabs_w[t] / 2, tabs_h[t] * .8)

    elif cur_tab == tab_names[3]:
        t = 3
        tabs_canvas[t].coords(txt_test, tabs_canvas[t].coords(headers[t])[0], tabs_canvas[t].coords(headers[t])[1] + 80)
        tabs_canvas[t].coords(win_expense_amount, tabs_w[t] / 2, tabs_h[t] / 2)
        tabs_canvas[t].coords(win_sbmt_expense_amount, tabs_canvas[t].coords(win_expense_amount)[0], tabs_canvas[t].coords(win_expense_amount)[1] + 45)
        tabs_canvas[t].coords(win_dropdown_cats, tabs_canvas[t].coords(win_expense_amount)[0] + 290, tabs_canvas[t].coords(win_expense_amount)[1])
        tabs_canvas[t].coords(user_info[t], tabs_w[t] / 2, tabs_h[t] * .8)

    elif cur_tab == tab_names[4]:
        t = 4
        report_display.config(width=round(tabs_w[t] * .11), height=tabs_h[t] / 21)
        tabs_canvas[t].coords(win_report_all, report_frame.winfo_x() + 74, (report_frame.winfo_y() + report_frame.winfo_reqheight()) + 5)
        tabs_canvas[t].coords(win_report_expenses, tabs_canvas[t].coords(win_report_all)[0] + btn_report_expenses.winfo_reqwidth(), tabs_canvas[t].coords(win_report_all)[1])
        tabs_canvas[t].coords(win_month, tabs_canvas[t].coords(win_report_expenses)[0] + 220, tabs_canvas[t].coords(win_report_all)[1] + 2)
        tabs_canvas[t].coords(txt_months, tabs_canvas[t].coords(win_report_expenses)[0] + 140, tabs_canvas[t].coords(win_month)[1])
        tabs_canvas[t].coords(txt_year, tabs_canvas[t].coords(win_month)[0] + 100, tabs_canvas[t].coords(win_year)[1])
        tabs_canvas[t].coords(win_year, tabs_canvas[t].coords(txt_year)[0] + 90, tabs_canvas[t].coords(win_month)[1])


# The logout button was getting a focus box for some reason, this fixed it.
def tab_change(event):
    tabControl.focus()
    # This guarantees that elements are displayed correctly on tab change
    try:
        drp_cats.set(Window.dat_dropdown_categories[0])
    except IndexError:
        drp_cats.set('')

    # Make sure values don't persist on tab change
    entry_username.delete(0, tk.END)
    entry_pass.delete(0, tk.END)
    entry_income.delete(0, tk.END)
    entry_expense_amount.delete(0, tk.END)
    entry_expense_cat.delete(0, tk.END)
    entry_expense_desc.delete("1.0", "end-1c")
    try:
        for i in range(num_tabs + 1):
            if i == 1:
                revert_text(tabs_canvas[i], txt_user_info2)
            revert_text(tabs_canvas[i], user_info[i])
    except IndexError:
        pass
    window_adjustment(None)
    root.update()


def hide_tabs():
    tab_count = tabControl.index('end')
    for j in range(1, tab_count):
        tabControl.tab(j, state="hidden")


def show_tabs():
    tab_count = tabControl.index('end')
    for j in range(1, tab_count):
        tabControl.tab(j, state="normal")


if __name__ == "__main__":
    # This is a master control for the number and names of tabs
    # >>> THE NUMBER OF TABS AND THE NUMBER OF STRINGS IN tab_names MUST MATCH <<<
    num_tabs = 5
    tab_names = ["Home", "Set Money", "Expense Tagger", "Add Expense", "Report View"]
    # How long the messages are displayed in ms
    user_info_timer = 5000
    # Needed arrays
    tabs_w = []
    tabs_h = []
    # need to initialize the array to be the size of the number of tabs so that I can change
    # the values and not append them elsewhere in the code.
    for i in range(num_tabs):
        tabs_w.append(0)
        tabs_h.append(0)

    obj_tabs = []
    tabs = []
    tabs_canvas = []
    # These are elements that appear on every page.
    headers = []
    user_info = []
    logouts = []
    logouts_windows = []

    root = tk.Tk()
    # Initializing data class variables
    Window.dat_user = tk.StringVar()
    Window.dat_password = tk.StringVar()
    Window.dat_balance = tk.StringVar()
    Window.dat_income = tk.StringVar()
    Window.dat_expense_cat = tk.StringVar()
    Window.dat_expense_amount = tk.StringVar()
    Window.dat_year = tk.IntVar()
    # This is the style sheet for the ttk module
    style = ttk.Style()
    style.theme_create("CustomStyle", parent='classic',
                       settings={
                           "TNotebook": {"configure": {"background": 'light grey'}},
                           "TNotebook.Tab": {
                               "configure": {"padding": [20, 5],
                                             "background": '#5E819D'},
                               "map": {"background": [("selected", '#6699CC'), ("active", '#9ECFFF')]}
                           },
                           "TCombobox": {
                               "configure": {
                                   "arrowsize": 10,
                                   "selectbackground": "white",
                                   "fieldbackground": "white",
                                   "selectforeground": "black",
                                   "arrowanchor": "s",
                               }
                           }
                       })
    style.theme_use("CustomStyle")
    # Save in case I want to see what themes exist
    # print(style.theme_names())

    # Fixed variables for text and labels
    # I have this here so that we can easily change elements as needed

    # Window Configuration
    root.title(Strings.title)
    root.geometry(f"{win_w}x{win_h}")
    root.minsize(win_w, win_h)

    # Make false to stop user from resizing window
    root.resizable(width=True, height=True)

    # Tab management variables
    tabControl = ttk.Notebook(root)

    for i in range(0, num_tabs):
        obj_tabs.append(TabManager.Tab(root, tabControl))
        obj_tabs[i].create_tab()
        tabs.append(obj_tabs[i].get_tab())
        tabs_canvas.append(obj_tabs[i].get_canvas())
        # Common element instantiation
        headers.append(tabs_canvas[i].create_text(0, 0, anchor='n', font=("Candara", 40), text=Strings.title))
        user_info.append(tabs_canvas[i].create_text(0, 0, anchor='n', font=("Candara Light", 12), text=''))
        logouts.append(tk.Button(tabs[i], text="Logout", state="disabled", width=20, command=lambda: app_btn_manager(3)))
        logouts_windows.append(tabs_canvas[i].create_window(0, 0, anchor='se', window=logouts[i]))

    # Tab 1 content
    txt_splash = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 36), text=Strings.splash)
    txt_disclaimer = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 10), justify='center', text=Strings.disclaimer)
    txt_username = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 12), text=Strings.username)
    txt_password = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 12), text=Strings.password)
    entry_username = tk.Entry(tabs[0], width=40, font=("Candara Light", 12), textvariable=Window.dat_user)
    entry_pass = tk.Entry(tabs[0], show="*", width=40, font=("Candara Light", 12), textvariable=Window.dat_password)

    btn_login = tk.Button(tabs[0], text="Login", width=20, command=lambda: app_btn_manager(1))
    btn_create_user = tk.Button(tabs[0], text="New User", width=20, command=lambda: app_btn_manager(2))

    win_login_display = tabs_canvas[0].create_window(0, 0, anchor='center', window=btn_login)
    win_create_user_display = tabs_canvas[0].create_window(0, 0, anchor='center', window=btn_create_user)

    win_username_display = tabs_canvas[0].create_window(0, 0, anchor='n', window=entry_username)
    win_pass_display = tabs_canvas[0].create_window(0, 0, anchor='n', window=entry_pass)
    # >>> Tab 1 Content END <<<

    # Tab 2 Content
    txt_money_disclaimer = tabs_canvas[1].create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center', text=Strings.money_disclaimer)
    txt_balance_desc = tabs_canvas[1].create_text(0, 0, anchor='center', font=("Candara Light", 12), justify='center', text=Strings.balance_desc)
    txt_income_desc = tabs_canvas[1].create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center', text=Strings.income_desc)
    txt_user_info2 = tabs_canvas[1].create_text(0, 0, anchor='n', font=("Candara Light", 12), text='')
    entry_income = tk.Entry(tabs[1], width=40, font=("Candara Light", 12), textvariable=Window.dat_income)
    entry_balance = tk.Entry(tabs[1], width=40, font=("Candara Light", 12), textvariable=Window.dat_balance)
    btn_sbmt_money = tk.Button(tabs[1], text="Submit", width=20, anchor='center', command=lambda: app_btn_manager(4))

    win_balance_display = tabs_canvas[1].create_window(0, 0, anchor='center', window=entry_balance)
    win_income_display = tabs_canvas[1].create_window(0, 0, anchor='n', window=entry_income)
    win_sbmt_money_display = tabs_canvas[1].create_window(0, 0, anchor='n', window=btn_sbmt_money)
    # >>> Tab 2 Content END <<<

    # Tab 3 Content
    entry_expense_cat = tk.Entry(tabs[2], width=40, font=("Candara Light", 12), textvariable=Window.dat_expense_cat)
    entry_expense_desc = tk.Text(tabs[2], wrap=tk.WORD, font=("Candara Light", 12), height=5, width=40)
    btn_sbmt_expense = tk.Button(tabs[2], width=20, font=("Candara Light", 12), text="Submit", command=lambda: app_btn_manager(5))
    txt_tagger_desc = tabs_canvas[2].create_text(0, 0, anchor='center', font=("Candara Light", 12), justify='center', text=Strings.expense_category_desc)
    txt_expense_cat = tabs_canvas[2].create_text(0, 0, anchor='e', font=("Candara Light", 12), justify='center', text=Strings.cat)
    txt_expense_desc = tabs_canvas[2].create_text(0, 0, anchor='e', font=("Candara Light", 12), justify='center', text=Strings.cat_desc)

    win_expense_cat = tabs_canvas[2].create_window(0, 0, anchor='center', window=entry_expense_cat)
    win_expense_desc = tabs_canvas[2].create_window(0, 0, anchor='n', window=entry_expense_desc)
    win_sbmt_expense = tabs_canvas[2].create_window(0, 0, anchor='s', window=btn_sbmt_expense)
    # >>>Tab 3 Content End

    # Tab 4 Content
    drp_cats = ttk.Combobox(tabs[3], values=Window.dat_dropdown_categories, state='readonly', font=("Candara Light", 12))
    txt_test = tabs_canvas[3].create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center', text=Strings.expense_disclaimer)
    entry_expense_amount = tk.Entry(tabs[3], width=40, font=("Candara Light", 12), textvariable=Window.dat_expense_amount)
    btn_sbmt_expense_amount = tk.Button(tabs[3], text="Submit", width=20, anchor='center', command=lambda: app_btn_manager(6))

    win_expense_amount = tabs_canvas[3].create_window(0, 0, anchor='center', window=entry_expense_amount)
    win_sbmt_expense_amount = tabs_canvas[3].create_window(0, 0, anchor='center', window=btn_sbmt_expense_amount)
    win_dropdown_cats = tabs_canvas[3].create_window(0, 0, anchor='center', window=drp_cats)
    # >>>Tab 4 Content End

    # Tab 5 Content
    # Needs buttons to select data sets
    report_frame = tk.Frame(tabs[4])
    report_frame.place(relx=.5, rely=.5, anchor='center')
    report_display = tk.Text(report_frame, wrap='none')
    report_display.pack(expand=True)
    # Set default value for year
    Window.dat_year.set(2024)
    txt_months = tabs_canvas[4].create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center', text=Strings.lbl_months)
    drp_months = ttk.Combobox(tabs[4], values=Window.months, state='readonly', font=("Candara Light", 12), width=5)
    # Set default value for month
    drp_months.set(Window.months[0])

    txt_year = tabs_canvas[4].create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center', text=Strings.lbl_year)
    entry_year = tk.Entry(tabs[4], width=5, justify='center', font=("Candara Light", 12), textvariable=Window.dat_year)

    # Buttons for getting different reports
    btn_report_all = tk.Button(tabs[4], text="Generate Report", width=20, anchor='center', command=lambda: report_event_manager(1))
    btn_report_expenses = tk.Button(tabs[4], text="Expense Breakdown", width=20, anchor='center', command=lambda: report_event_manager(2))
    # Button windows
    win_report_all = tabs_canvas[4].create_window(0, 0, anchor="n", window=btn_report_all)
    win_report_expenses = tabs_canvas[4].create_window(0, 0, anchor="n", window=btn_report_expenses)
    win_month = tabs_canvas[4].create_window(0, 0, anchor='n', window=drp_months)
    win_year = tabs_canvas[4].create_window(0, 0, anchor='n', window=entry_year)

    scroll = tk.Scrollbar(tabs_canvas[4], orient='vertical', command=report_display.yview)
    report_display.config(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    report_display.tag_configure("center", justify="center")
    report_display.config(state="disabled")
    # >>>Tab 5 Content End
    # Add the tabs to the tab controller
    for i in range(0, num_tabs):
        tabControl.add(tabs[i], text=tab_names[i])

    tabControl.pack(fill=tk.BOTH, expand=True)
    # This is what calls the window adjust definition when the window is configured.
    hide_tabs()
    # This bind was for debugging
    # drp_cats.bind("<<ComboboxSelected>>", dropdown_control)
    root.bind('<Configure>', window_adjustment)
    tabControl.bind("<<NotebookTabChanged>>", tab_change)
    root.mainloop()
