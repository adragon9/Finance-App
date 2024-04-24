import sqlite3
import tkinter as tk
from tkinter import ttk

import TabManager
import user
from AppData import Window

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
    backup_db = sqlite3.connect(f'Users-backup.db')
    connection.backup(backup_db)
    backup_db.close()
    connection.close()


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
            btn_login.configure(state="disabled")
            btn_create_user.configure(state="disabled")
            # This enables all the logout buttons
            for i in range(0, num_tabs):
                logouts[i].configure(state='normal')
            # Inform user, update displays, clear inputs
            show_tabs()
            tabs_canvas[0].itemconfig(txt_splash, text=f"Welcome, {cur_user.get_current_user()}")
            tabs_canvas[0].itemconfig(txt_user_info1, text=str_success)
            entry_username.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))
        else:
            tabs_canvas[0].itemconfig(txt_user_info1, text=str_fail_login)
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

        # Create user event
    elif event_id == 2:
        status = cur_user.create_user()
        print(status)
        if status:
            tabs_canvas[0].itemconfig(txt_user_info1, text=str_success_create)
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

        elif not status and cur_user.get_current_user() is None and cur_user.get_current_password() is None:
            tabs_canvas[0].itemconfig(txt_user_info1, text=f"{str_blank}: BOTH")
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

        elif not status and cur_user.get_current_password() is None:
            tabs_canvas[0].itemconfig(txt_user_info1, text=f"{str_blank}: Password")
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

        elif not status and cur_user.get_current_user() is None:
            tabs_canvas[0].itemconfig(txt_user_info1, text=f"{str_blank}: USERNAME")
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

        elif not status and cur_user.get_current_password() is None:
            tabs_canvas[0].itemconfig(txt_user_info1, text=f"{str_blank}: Password")
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

        else:
            tabs_canvas[0].itemconfig(txt_user_info1, text=str_fail_create)
            root.after(3000, lambda: revert_text(tabs_canvas[0], txt_user_info1))

    # Logout event
    elif event_id == 3:
        # Clear saved user and password
        Window.saved_dat_user = None
        Window.saved_dat_pass = None
        Window.saved_dat_balance = None

        # Clear ALL entry boxes on logout
        entry_username.delete(0, tk.END)
        entry_pass.delete(0, tk.END)
        entry_balance.delete(0, tk.END)
        entry_expense_cat.delete(0, tk.END)
        entry_expense_desc.delete("1.0", "end-1c")

        # print(Window.saved_dat_user, Window.saved_dat_pass, Window.saved_dat_balance)
        btn_login.configure(state="normal")
        btn_create_user.configure(state="normal")
        for i in range(0, num_tabs):
            logouts[i].configure(state='disabled')
        hide_tabs()
        tabs_canvas[0].itemconfig(txt_splash, text=str_splash)
    # Submit user balance
    elif event_id == 4:
        # print(Window.saved_dat_user, Window.saved_dat_pass) <-- used to check if the username and pass was being saved
        if Window.current_user is not None:
            data_backup()
            balance = Window.current_user.set_balance(entry_balance.get())
            if balance:
                tabs_canvas[1].itemconfig(txt_user_info2,
                                          text=f"{str_success_balance}${Window.current_user.get_balance():,.2f}")
                Window.saved_dat_balance = Window.current_user.get_balance()
                entry_balance.delete(0, tk.END)
                root.after(3000, lambda: revert_text(tabs_canvas[1], txt_user_info2))
            else:
                tabs_canvas[1].itemconfig(txt_user_info2,
                                          text=f"{str_fail_balance}${Window.current_user.get_balance():,.2f}")
                Window.saved_dat_balance = Window.current_user.get_balance()
                entry_balance.delete(0, tk.END)
                root.after(3000, lambda: revert_text(tabs_canvas[1], txt_user_info2))
        else:
            print("No user logged in")
    # Submit category
    elif event_id == 5:
        Window.saved_dat_expense_desc = entry_expense_desc.get("1.0", "end-1c")
        Window.saved_dat_expense_cat = Window.dat_expense_cat.get()

        entry_expense_desc.delete("1.0", "end-1c")
        entry_expense_cat.delete(0, tk.END)

        if Window.saved_dat_expense_cat != '':
            print(Window.saved_dat_expense_cat, Window.saved_dat_expense_desc)
            Window.current_user.create_expense(Window.saved_dat_expense_cat, Window.saved_dat_expense_desc)


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
        tabs_canvas[t].coords(logouts_windows[t], tabs_w[t] - 10, tabs_h[t] - 10)

    # Needed to reduce flickering on tab change
    root.update_idletasks()
    # Hopefully this will lead to some optimization down the line.
    # Instead of updating all elements it only updates the active tabs elements.
    cur_tab = tabControl.tab(tabControl.select(), "text")
    if cur_tab == tab_names[0]:
        # print('updating 1')
        # Readjusts elements to stay in the same position no matter window size
        tabs_canvas[0].coords(txt_splash, tabs_w[0] / 2, tabs_canvas[0].coords(headers[0])[1] + 80)
        tabs_canvas[0].coords(txt_disclaimer, tabs_w[0] * .5, tabs_canvas[0].coords(txt_splash)[1] + 60)
        tabs_canvas[0].coords(win_login_display, tabs_w[0] / 2, tabs_h[0] * .8)
        tabs_canvas[0].coords(win_create_user_display, tabs_w[0] / 2, btn_login.winfo_y() + 45)
        tabs_canvas[0].coords(txt_username, entry_username.winfo_x() - 40, entry_username.winfo_y())
        tabs_canvas[0].coords(win_username_display, tabs_w[0] / 2, tabs_h[0] * .5)
        tabs_canvas[0].coords(txt_password, entry_pass.winfo_x() - 40, entry_pass.winfo_y())
        tabs_canvas[0].coords(win_pass_display, tabs_w[0] / 2, entry_username.winfo_y() + 30)
        tabs_canvas[0].coords(txt_user_info1, tabs_w[0] / 2, entry_username.winfo_y() + 60)

    elif cur_tab == tab_names[1]:
        # print('updating 2')
        tabs_canvas[1].coords(txt_balance_des, tabs_canvas[1].coords(headers[1])[0],
                              tabs_canvas[1].coords(headers[1])[1] + 80)
        tabs_canvas[1].coords(win_balance_display, tabs_w[1] / 2, tabs_h[1] / 2)
        tabs_canvas[1].coords(win_sbmt_bal_display, tabs_canvas[1].coords(win_balance_display)[0],
                              tabs_canvas[1].coords(win_balance_display)[1] + 45)
        tabs_canvas[1].coords(txt_user_info2, tabs_canvas[1].coords(win_sbmt_bal_display)[0],
                              tabs_canvas[1].coords(win_sbmt_bal_display)[1] + 45)

    elif cur_tab == tab_names[2]:
        tabs_canvas[2].coords(win_expense_cat, tabs_w[2] / 2, tabs_h[2] / 2)
        tabs_canvas[2].coords(win_expense_desc, tabs_w[2] / 2, tabs_canvas[2].coords(win_expense_cat)[1] + 10)
        tabs_canvas[2].coords(win_sbmt_expense, tabs_w[2] / 2, tabs_h[2] - 10)


# The logout button was getting a focus box for some reason, this fixed it.
def tab_change(event):
    tabControl.focus()


def hide_tabs():
    tab_count = tabControl.index('end')
    for i in range(1, tab_count):
        tabControl.tab(i, state="hidden")


def show_tabs():
    tab_count = tabControl.index('end')
    for i in range(1, tab_count):
        tabControl.tab(i, state="normal")


if __name__ == "__main__":
    # This is a master control for the number and names of tabs
    # >>> THE NUMBER OF TABS AND THE NUMBER OF STRINGS IN tab_names MUST MATCH <<<
    num_tabs = 3
    tab_names = ["Home", "Set Balance", "Expenses"]
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
    logouts = []
    logouts_windows = []

    root = tk.Tk()
    # Initializing data class variables
    Window.dat_user = tk.StringVar()
    Window.dat_password = tk.StringVar()
    Window.dat_balance = tk.StringVar()
    Window.dat_expense_cat = tk.StringVar()

    # This is the style sheet for the ttk module
    style = ttk.Style()
    style.theme_create("CustomStyle", parent='classic',
                       settings={
                           "TNotebook": {"configure": {"background": 'light grey'}},
                           "TNotebook.Tab": {
                               "configure": {"padding": [20, 5],
                                             "background": '#5E819D'},
                               "map": {"background": [("selected", '#6699CC'), ("active", '#9ECFFF')]}
                           }
                       })
    style.theme_use("CustomStyle")

    # Save in case I want to see what themes exist
    # print(style.theme_names())

    # Fixed variables for text and labels
    # I have this here so that we can easily change elements as needed
    str_title = "Finance Tracker"
    str_splash = "WELCOME TO THE APPLICATION"
    str_disclaimer = "Make sure to write down your password, editing has not been implemented."
    str_balance_desc = "You may manually set your balance here.\nNOTE: THIS WILL OVERWRITE YOUR PREVIOUS BALANCE."
    str_success_create = "User created!"
    str_fail_login = "Match not found login failed"
    str_success = "Login successful"
    str_blank = "Entry boxes not filled out"
    str_success_balance = "You successfully set your balance too: "
    str_fail_balance = "Your balance input was not valid balance set to: "
    str_fail_create = "User already exists or some other error has occurred user not created."
    str_username = "Username"
    str_password = "Password"

    # Window Configuration
    root.title(str_title)
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
        headers.append(tabs_canvas[i].create_text(0, 0, anchor='n', font=("Candara", 40), text=str_title))
        logouts.append(
            tk.Button(tabs[i], text="Logout", state="disabled", width=20, command=lambda: app_btn_manager(3)))
        logouts_windows.append(tabs_canvas[i].create_window(0, 0, anchor='se', window=logouts[i]))

    # Tab 1 content
    txt_splash = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 36), text=str_splash)
    txt_disclaimer = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 10), text=str_disclaimer)
    txt_username = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 12), text=str_username)
    txt_password = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 12), text=str_password)
    txt_user_info1 = tabs_canvas[0].create_text(0, 0, anchor='n', font=("Candara Light", 12), text='')
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
    txt_balance_des = tabs_canvas[1].create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center',
                                                 text=str_balance_desc)
    txt_user_info2 = tabs_canvas[1].create_text(0, 0, anchor='n', font=("Candara Light", 12), text='')
    entry_balance = tk.Entry(tabs[1], width=40, font=("Candara Light", 12), textvariable=Window.dat_balance)
    btn_sbmt_bal = tk.Button(tabs[1], text="Submit", width=20, anchor='center', command=lambda: app_btn_manager(4))

    win_balance_display = tabs_canvas[1].create_window(0, 0, anchor='center', window=entry_balance)
    win_sbmt_bal_display = tabs_canvas[1].create_window(0, 0, anchor='center', window=btn_sbmt_bal)
    # >>> Tab 2 Content END <<<

    # Tab 3 Content
    entry_expense_cat = tk.Entry(tabs[2], width=40, font=("Candara Light", 12), textvariable=Window.dat_expense_cat)
    entry_expense_desc = tk.Text(tabs[2], wrap=tk.WORD, font=("Candara Light", 12), height=5, width=40)
    btn_sbmt_expense = tk.Button(tabs[2], width=20, font=("Candara Light", 12), text="Submit",
                                 command=lambda: app_btn_manager(5))

    win_expense_cat = tabs_canvas[2].create_window(0, 0, anchor='s', window=entry_expense_cat)
    win_expense_desc = tabs_canvas[2].create_window(0, 0, anchor='n', window=entry_expense_desc)
    win_sbmt_expense = tabs_canvas[2].create_window(0, 0, anchor='s', window=btn_sbmt_expense)
    # >>>Tab 3 Content End

    # Add the tabs to the tab controller
    for i in range(0, num_tabs):
        tabControl.add(tabs[i], text=tab_names[i])

    tabControl.pack(fill=tk.BOTH, expand=True)
    # This is what calls the window adjust definition when the window is configured.
    hide_tabs()
    root.bind('<Configure>', window_adjustment)
    tabControl.bind("<<NotebookTabChanged>>", tab_change)
    root.mainloop()
