import tkinter as tk
from tkinter import ttk

import security

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


def activate_security(event_id):
    sec = security.Security(entry_username.get(), entry_pass.get(), entry_username, entry_pass, tabControl)
    if event_id == 1:
        sec.login()
        tab1_canvas.itemconfig(txt_splash, text=f"Welcome, {sec.get_current_user()[1]}")
    elif event_id == 2:
        sec.create_user()


# Ensures that all elements stay in relative positions when window size is changed
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
    tab1_canvas.coords(win_create_user_display, tab1_w / 2, btn_login.winfo_y() + 45)
    tab1_canvas.coords(txt_username, entry_username.winfo_x() - 40, entry_username.winfo_y())
    tab1_canvas.coords(win_username_display, tab1_w / 2, tab1_h * .5)
    tab1_canvas.coords(txt_password, entry_pass.winfo_x() - 40, entry_pass.winfo_y())
    tab1_canvas.coords(win_pass_display, tab1_w / 2, entry_username.winfo_y() + 30)

    # Tab2 canvas manager
    tab2_w = tab2_canvas.winfo_width()
    tab2_h = tab2_canvas.winfo_height()

    tab2_canvas.coords(win_header2, tab2_w / 2, 5)


def hide_tabs():
    tab_count = tabControl.index('end')
    for i in range(1, tab_count):
        tabControl.tab(i, state="hidden")


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
    title = "Finance Tracker"
    splash = "WELCOME TO THE APPLICATION"
    disclaimer = "Make sure to write down your password, editing has not been implemented."
    lbl_username = "Username"
    lbl_password = "Password"

    # Window Configuration
    root.title(title)
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
    txt_header1 = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara", 32), text=title)
    txt_splash = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 36), text=splash)
    txt_disclaimer = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 10), text=disclaimer)
    txt_username = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), text=lbl_username)
    txt_password = tab1_canvas.create_text(0, 0, anchor='n', font=("Candara Light", 12), text=lbl_password)

    entry_username = tk.Entry(tab1, width=40, font=("Candara Light", 12))
    entry_pass = tk.Entry(tab1, show="*", width=40, font=("Candara Light", 12))
    # Creates a security object for logging in and creating users
    btn_login = tk.Button(tab1, text="Login", width=20, anchor='center', command=lambda: activate_security(1))
    btn_create_user = tk.Button(tab1, text="New User", width=20, anchor='center', command=lambda: activate_security(2))

    win_login_display = tab1_canvas.create_window(0, 0, anchor='center', window=btn_login)
    win_create_user_display = tab1_canvas.create_window(0, 0, anchor='center', window=btn_create_user)
    win_username_display = tab1_canvas.create_window(0, 0, anchor='n', window=entry_username)
    win_pass_display = tab1_canvas.create_window(0, 0, anchor='n', window=entry_pass)

    # Tab 2 Content
    win_header2 = tab2_canvas.create_text(root.winfo_width() / 2, 5, anchor='n', font=("Candara", 32), text=title)

    # Add the tabs to the tab controller
    tabControl.add(tab1, text="Home")
    tabControl.add(tab2, text="Tab 2")
    tabControl.pack(fill=tk.BOTH, expand=True)
    # This is what calls the window adjust definition when the window is configured.
    hide_tabs()
    root.bind('<Configure>', window_adjustment)
    root.mainloop()
