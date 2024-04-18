import sqlite3
import datetime as dt
import tkinter as tk
from tkinter import ttk


class User:
    def __init__(self, username: str, password: str, user_entry: tk.Entry, pass_entry: tk.Entry, tabs: ttk.Notebook):
        """
        user_entry and pass_entry are the entry boxes that contain the username and password.
        tabs is the Notebook that has your tabs in it.
        :param username:
        :param password:
        :param user_entry:
        :param pass_entry:
        :param tabs:
        """
        self.user = username
        self.current_user = username
        self.password = password
        self.user_entry = user_entry
        self.pass_entry = pass_entry
        self.tabs = tabs
        self.balance = 0.0

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
            password STRING,
            balance MONEY)""")

            date = dt.datetime.now()

            try:
                cursor.execute("""
                INSERT INTO users(
                user_name,
                date_created,
                password,
                balance) VALUES(?,?,?,?)""", (self.user, date, self.password, self.balance))
            except sqlite3.IntegrityError:
                print("USERNAME TAKEN")

            connection.commit()

            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        connection.close()
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        if self.user == '':
            self.user = None
        elif not self.user.isalpha():
            self.user = None

        if self.password == '':
            self.password = None

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
                    print(check[0])
                    self.current_user = check[0]
            else:
                print("no match")

        connection.close()
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def get_current_user(self):
        return self.current_user

    def get_income(self):
        return self.balance

    def set_balance(self, balance):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        try:
            self.balance = float(balance)
        except ValueError:
            self.balance = 0.0

        print(self.user)
        print(self.current_user)

        cursor.execute("""UPDATE users
        SET balance = ?
        WHERE user_name = ?""", (self.balance, self.current_user))

        connection.commit()
        connection.close()
