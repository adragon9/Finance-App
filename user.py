import datetime as dt
import sqlite3
import tkinter as tk


class User:
    def __init__(self, username: str, password: str, user_entry: tk.Entry, pass_entry: tk.Entry):
        """
        user_entry and pass_entry are the entry boxes that contain the username and password.
        tabs is the Notebook that has your tabs in it.
        :param username:
        :param password:
        :param user_entry:
        :param pass_entry:
        :param tabs:
        """
        self.username = username
        self.password = password
        self.user_entry = user_entry
        self.pass_entry = pass_entry
        self.balance = 0.0

    def create_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        if self.username == '':
            self.username = None
        elif not self.username.isalnum():
            self.username = None
        if self.password == '':
            self.password = None

        if self.username is not None and self.password is not None:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            user_name TEXT PRIMARY KEY,
            date_created DATETIME,
            password TEXT,
            balance MONEY)""")

            date = dt.datetime.now()

            try:
                cursor.execute("""
                INSERT INTO users(
                user_name,
                date_created,
                password,
                balance) VALUES(?,?,?,?)""", (self.username, date, self.password, self.balance))
            except sqlite3.IntegrityError:
                print("USERNAME TAKEN")
                connection.close()
                self.user_entry.delete(0, tk.END)
                self.pass_entry.delete(0, tk.END)
                return False
            connection.commit()

            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        connection.close()
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        return True

    def login(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        if self.username == '':
            self.username = None
        elif not self.username.isalnum():
            self.username = None

        if self.password == '':
            self.password = None

        if self.username is not None and self.password is not None:
            cursor.execute((f"""SELECT
            user_name, 
            password 
            FROM users 
            WHERE user_name = ? AND password = ?"""), (self.username, self.password))

            check = cursor.fetchone()
            if check:
                print(f"found match: Name {check[0]},Password {check[1]}")
                connection.close()
                self.user_entry.delete(0, tk.END)
                self.pass_entry.delete(0, tk.END)
                return True
            else:
                self.username = None
                print("no match")
                connection.close()
                self.user_entry.delete(0, tk.END)
                self.pass_entry.delete(0, tk.END)
                return False

    def get_current_user(self):
        return self.username

    def get_current_password(self):
        return self.password

    def get_income(self):
        return self.balance

    def set_balance(self, balance):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        success = None

        try:
            self.balance = float(balance)
            # remove for final build ;)
            if self.balance > 9999999:
                print("Balance Set, look at you high roller.")
            else:
                print("Balance Set")

            cursor.execute("""UPDATE users
            SET balance = ?
            WHERE user_name = ?""", (self.balance, self.username))

            connection.commit()
            connection.close()
            success = True
        except ValueError:
            print("A problem occurred")
            success = False

        # Just in case something goes wrong
        if success is None:
            success = False

        return success

    def get_balance(self):
        return self.balance
