import sqlite3
import datetime as dt
import tkinter as tk
from tkinter import ttk


class Security:
    def __init__(self, user: str, password: str, user_entry: tk.Entry, pass_entry: tk.Entry, tabs: ttk.Notebook):
        """
        user_entry and pass_entry are the entry boxes that contain the username and password.
        tabs is the Notebook that has your tabs in it.
        :param user:
        :param password:
        :param user_entry:
        :param pass_entry:
        :param tabs:
        """
        self.current_user = None
        self.user = user
        self.password = password
        self.user_entry = user_entry
        self.pass_entry = pass_entry
        self.tabs = tabs

    def create_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        if self.user == '':
            self.user = None
        elif not self.user.isalnum():
            self.user = None
        if self.password == '':
            self.password = None

        if self.user is not None and self.password is not None:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            user_name STRING PRIMARY KEY,
            date_created DATETIME,
            password STRING)""")

            date = dt.datetime.now()
            user = self.user
            password = self.password
            try:
                cursor.execute("""
                INSERT INTO users(
                user_name,
                date_created,
                password) VALUES(?,?,?)""", (user, date, password))
            except sqlite3.IntegrityError:
                print("USERNAME TAKEN")

            connection.commit()

            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        if self.user == '':
            user = None
        elif not self.user.isalpha():
            user = None

        if self.password == '':
            password = None

        if self.user is not None and self.password is not None:
            cursor.execute((f"""SELECT
            user_name, 
            password 
            FROM users 
            WHERE user_name = ? AND password = ?"""), (self.user, self.password))

            check = cursor.fetchone()

            if check:
                print(f"found match: Name {check[0]},Password {check[1]}")
                tab_count = self.tabs.index('end')
                for i in range(1, tab_count):
                    self.tabs.tab(i, state="normal")
                    self.current_user = check
            else:
                print("no match")

        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def get_current_user(self):
        return self.current_user
