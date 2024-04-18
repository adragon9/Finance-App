import tkinter as tk
from tkinter import ttk

import user

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


def app_btn_manager(event_id):
    # Needed so that the entire program has access to the current active use.
    # This is due to a lack of foresight as every time this event manager got called the cur_user var got overwritten
    global saved_user
    cur_user = user.User(entry_username.get(), entry_pass.get(), entry_username, entry_pass)
    # Login button pressed on home tab
    if event_id == 1:
        cur_user.login()
        if cur_user.get_current_user() is not None:
            show_tabs()
            tab1_canvas.itemconfig(txt_splash, text=f"Welcome, {cur_user.get_current_user()}")
            btn_login.configure(state="disabled")
            btn_create_user.configure(state="disabled")
            btn_logout1.configure(state="normal")
            btn_logout2.configure(state="normal")
            tab1_canvas.itemconfig(txt_user_info1, text=str_success)
            root.after(3000, lambda: revert_text(tab1_canvas, txt_user_info1))
            saved_user = cur_user
            print("saved_user = " + saved_user.get_current_user())
        else:
            tab1_canvas.itemconfig(txt_user_info1, text=str_fail_login)
            root.after(3000, lambda: revert_text(tab1_canvas, txt_user_info1))
            print("Not logged in")

    # New user button pressed on home tab
    elif event_id == 2:
        status = cur_user.create_user()
        print()
        if cur_user.get_current_user() is not None and cur_user.get_current_password() is not None:
            if status and cur_user.get_current_user() is not None:
                tab1_canvas.itemconfig(txt_user_info1, text=str_success_create)
                root.after(3000, lambda: revert_text(tab1_canvas, txt_user_info1))
            elif not status and cur_user.get_current_user() is not None:
                tab1_canvas.itemconfig(txt_user_info1, text=str_fail_create)
                root.after(3000, lambda: revert_text(tab1_canvas, txt_user_info1))
        else:
            tab1_canvas.itemconfig(txt_user_info1, text=str_blank)
            root.after(3000, lambda: revert_text(tab1_canvas, txt_user_info1))

    # Logout button pressed on home tab
    elif event_id == 3:
        tab1_canvas.itemconfig(txt_splash, text=str_splash)
        btn_login.configure(state="normal")
        btn_create_user.configure(state="normal")
        btn_logout1.configure(state="disabled")
        btn_logout2.configure(state="disabled")
        hide_tabs()
        # Wanted to make sure that in when the logout is pressed that variable gets cleared
        saved_user = None

    elif event_id == 4:
        balance = saved_user.set_balance(entry_balance.get())
        if balance:
            tab2_canvas.itemconfig(txt_user_info2, text=f"{str_success_balance}{saved_user.get_balance():.2f}")
            root.after(3000, lambda: revert_text(tab2_canvas, txt_user_info2))


"""
Ensures that all elements stay in relative positions when window size is changed
The event is also a necessary parameter for this function to call correctly as it is needed by .bind()
"""


def window_adjustment(event):
    """
    This gets the entire window size which is not the size of the tab container
    If activated it causes elements to teleport a little which was annoying
    width = event.width
    height = event.height
    print(tab1_canvas.winfo_geometry())
    """
    # Tab1 canvas manager
    tab1_w = tab1_canvas.winfo_width()
    tab1_h = tab1_canvas.winfo_height()
    # Readjusts elements to stay in the same position no matter window size
    tab1_canvas.coords(txt_header1, tab1_w / 2, 5)
    tab1_canvas.coords(txt_splash, tab1_w / 2, tab1_h * .1)
    tab1_canvas.coords(txt_disclaimer, tab1_w * .5, tab1_canvas.coords(txt_splash)[1] + 60)
    tab1_canvas.coords(win_login_display, tab1_w / 2, tab1_h * .8)
    tab1_canvas.coords(win_logout_display1, tab1_w - 10, tab1_h - 10)
    tab1_canvas.coords(win_create_user_display, tab1_w / 2, btn_login.winfo_y() + 45)
    tab1_canvas.coords(txt_username, entry_username.winfo_x() - 40, entry_username.winfo_y())
    tab1_canvas.coords(win_username_display, tab1_w / 2, tab1_h * .5)
    tab1_canvas.coords(txt_password, entry_pass.winfo_x() - 40, entry_pass.winfo_y())
    tab1_canvas.coords(win_pass_display, tab1_w / 2, entry_username.winfo_y() + 30)
    tab1_canvas.coords(txt_user_info1, tab1_w / 2, entry_username.winfo_y() + 60)

    # Tab2 canvas manager
    tab2_w = tab2_canvas.winfo_width()
    tab2_h = tab2_canvas.winfo_height()

    tab2_canvas.coords(txt_header2, tab2_w / 2, 5)
    tab2_canvas.coords(txt_balance_des, tab2_canvas.coords(txt_header2)[0], tab2_canvas.coords(txt_header2)[1] + 60)
    tab2_canvas.coords(win_balance_display, tab2_w / 2, tab2_h / 2)
    tab2_canvas.coords(win_sbmt_bal_display, tab2_canvas.coords(win_balance_display)[0],
                       tab2_canvas.coords(win_balance_display)[1] + 45)
    tab2_canvas.coords(txt_user_info2, tab2_canvas.coords(win_sbmt_bal_display)[0], tab2_canvas.coords(win_sbmt_bal_display)[1] + 45)
    tab2_canvas.coords(win_logout_display2, tab1_w - 10, tab1_h - 10)


def hide_tabs():
    tab_count = tabControl.index('end')
    for i in range(1, tab_count):
        tabControl.tab(i, state="hidden")


def show_tabs():
    tab_count = tabControl.index('end')
    for i in range(1, tab_count):
        tabControl.tab(i, state="normal")


if __name__ == "__main__":
    root = tk.Tk()
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
    str_fail_balance = "Your balance was not updated"
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

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    # Tab 1 Canvas
    tab1_canvas = tk.Canvas(tab1)
    tab1_canvas.pack(fill=tk.BOTH, expand=True)
    # Tab 2 Canvas
    tab2_canvas = tk.Canvas(tab2)
    tab2_canvas.pack(fill=tk.BOTH, expand=True)

    root.update()
    tabControl.update()

    # Tab 1 content
    txt_header1 = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara", 32), text=str_title)
    txt_splash = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 36), text=str_splash)
    txt_disclaimer = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 10), text=str_disclaimer)
    txt_username = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), text=str_username)
    txt_password = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), text=str_password)
    txt_user_info1 = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), text='')
    entry_username = tk.Entry(tab1, width=40, font=("Candara Light", 12))
    entry_pass = tk.Entry(tab1, show="*", width=40, font=("Candara Light", 12))

    btn_login = tk.Button(tab1, text="Login", width=20, command=lambda: app_btn_manager(1))
    btn_create_user = tk.Button(tab1, text="New User", width=20, command=lambda: app_btn_manager(2))
    btn_logout1 = tk.Button(tab1, text="Logout", state="disabled", width=20, command=lambda: app_btn_manager(3))

    win_login_display = tab1_canvas.create_window(0, 0, anchor='center', window=btn_login)
    win_logout_display1 = tab1_canvas.create_window(0, 0, anchor='se', window=btn_logout1)
    win_create_user_display = tab1_canvas.create_window(0, 0, anchor='center', window=btn_create_user)

    win_username_display = tab1_canvas.create_window(0, 0, anchor='n', window=entry_username)
    win_pass_display = tab1_canvas.create_window(0, 0, anchor='n', window=entry_pass)
    # >>> Tab 1 Content END <<<

    # Tab 2 Content
    txt_header2 = tab2_canvas.create_text(0, 0, anchor='n', font=("Candara", 32), text=str_title)
    txt_balance_des = tab2_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), justify='center', text=str_balance_desc)
    txt_user_info2 = tab2_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), text='')
    entry_balance = tk.Entry(tab2, width=40, font=("Candara Light", 12))
    btn_sbmt_bal = tk.Button(tab2, text="Submit", width=20, anchor='center', command=lambda: app_btn_manager(4))
    btn_logout2 = tk.Button(tab2, text="Logout", state="disabled", width=20, command=lambda: app_btn_manager(3))

    win_balance_display = tab2_canvas.create_window(0, 0, anchor='center', window=entry_balance)
    win_sbmt_bal_display = tab2_canvas.create_window(0, 0, anchor='center', window=btn_sbmt_bal)
    win_logout_display2 = tab2_canvas.create_window(0, 0, anchor='se', window=btn_logout2)
    # >>> Tab 2 Content END <<<

    # Add the tabs to the tab controller
    tabControl.add(tab1, text="Home")
    tabControl.add(tab2, text="Set Balance")
    tabControl.pack(fill=tk.BOTH, expand=True)
    # This is what calls the window adjust definition when the window is configured.
    hide_tabs()
    root.bind('<Configure>', window_adjustment)
    root.mainloop()
