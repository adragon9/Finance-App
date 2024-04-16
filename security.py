import sqlite3
import datetime as dt
import tkinter as tk
from tkinter import ttk


def create_user(user: str, password: str, user_entry: tk.Entry, pass_entry: tk.Entry):
    connection = sqlite3.connect("Users.db")
    cursor = connection.cursor()
    if user == '':
        user = None
    elif not user.isalpha():
        user = None
    if password == '':
        password = None

    if user is not None and password is not None:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        date_created DATETIME,
        user_name STRING,
        password STRING)""")

        date = dt.datetime.now()
        user = user
        password = password

        cursor.execute("""
        INSERT INTO users(
        date_created,
        user_name,
        password) VALUES(?,?,?)""", (date, user, password))

        connection.commit()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)


def login(user: str, password: str, tabs: ttk.Notebook):
    """
    plan to have this return true if username and password match item in database
    :param tabs:
    :param user:
    :param password:
    :return:
    """
    connection = sqlite3.connect("Users.db")
    cursor = connection.cursor()

    if user == '':
        user = None
    elif not user.isalpha():
        user = None

    if password == '':
        password = None

    if user is not None and password is not None:
        cursor.execute((f"""SELECT 
        user_name, 
        password 
        FROM users 
        WHERE user_name = ? AND password = ?"""), (user, password))

        check = cursor.fetchone()

        if check:
            print("found match")
            tab_count = tabs.index('end')
            for i in range(1, tab_count):
                tabs.tab(i, state="normal")
        else:
            print("no match")



