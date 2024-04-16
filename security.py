import sqlite3
import datetime as dt
import tkinter as tk
from tkinter import ttk


class Security:
    def __init__(self, user: str, password: str, user_entry: tk.Entry, pass_entry: tk.Entry, tabs: ttk.Notebook):
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
            user = None
        elif not self.user.isalpha():
            user = None
        if self.password == '':
            password = None

        if self.user is not None and self.password is not None:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            date_created DATETIME,
            user_name STRING,
            password STRING)""")

            date = dt.datetime.now()
            user = self.user
            password = self.password

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

        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login(self):
        """
        plan to have this return true if username and password match item in database
        :param tabs:
        :param user:
        :param password:
        :return:
        """
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
            id, 
            user_name, 
            password 
            FROM users 
            WHERE user_name = ? AND password = ?"""), (self.user, self.password))

            check = cursor.fetchone()

            if check:
                print(f"found match: id {check[0]},Name {check[1]},Password {check[2]}")
                tab_count = self.tabs.index('end')
                for i in range(1, tab_count):
                    self.tabs.tab(i, state="normal")
                    self.current_user = check
            else:
                print("no match")

    def get_current_user(self):
        return self.current_user
