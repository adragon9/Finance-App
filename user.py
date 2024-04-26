import datetime
import datetime as dt
import sqlite3


class User:
    def __init__(self, username: str, password: str):
        """
        user_entry and pass_entry are the entry boxes that contain the username and password.
        tabs is the Notebook that has your tabs in it.
        :param username:
        :param password:
        """
        self.username = username
        self.password = password
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
            # Create ALL necessary tables here
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            user_name TEXT PRIMARY KEY,
            date_created DATETIME,
            password TEXT,
            balance MONEY)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS expense_categories(
            category_name TEXT,
            user_name TEXT,
            category_date DATE,
            category_desc TEXT,
            PRIMARY KEY(category_name, user_name),
            FOREIGN KEY (user_name) REFERENCES users(user_name))""")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
            expense_id INTEGER PRIMARY KEY,
            category_name TEXT,
            user_name TEXT,
            expense_amount MONEY,
            expense_added DATE,
            FOREIGN KEY(user_name) REFERENCES users(user_name),
            FOREIGN KEY(category_name) REFERENCES expense_categories(category_name))""")
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
                return False
            connection.commit()

            # Debug print remove later
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            connection.close()
            return True
        else:
            connection.close()
            return False

    def create_expense(self, expense_cat, expense_desc):
        if self.username != '':
            connection = sqlite3.connect('Users.db')
            cursor = connection.cursor()
            date = datetime.datetime.now()
            try:
                cursor.execute("""INSERT INTO expense_categories(
                category_name,
                user_name,
                category_date,
                category_desc) Values(?,?,?,?)""", (expense_cat, self.username, date, expense_desc))
            except sqlite3.IntegrityError:
                print("CATEGORY EXISTS")
                connection.close()
                return False

            connection.commit()
            connection.close()
            return True
        else:
            return False

    def add_expense(self, expense_cat, expense_amount):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        date = datetime.datetime.now()

        try:
            cursor.execute("""INSERT INTO expenses(
            category_name,
            user_name,
            expense_amount,
            expense_added) VALUE(?, ?, ?, ?""", (expense_cat, self.username, expense_amount, date))
        except sqlite3.IntegrityError:
            print("ID EXISTS")
            connection.close()
            return False

        connection.commit()
        connection.close()
        return True

    # Modify the login method to return True on successful login, and False otherwise
    def login(self):
        try:
            connection = sqlite3.connect("Users.db")
            cursor = connection.cursor()

            if self.username == '' or self.password == '':
                print("Invalid username or password")
                return False

            cursor.execute("""
                SELECT user_name, password 
                FROM users 
                WHERE user_name = ? AND password = ?""", (self.username, self.password))

            check = cursor.fetchone()

            if check:
                print(f"Login successful for user: {self.username}")
                connection.close()
                return True
            else:
                print("Invalid username or password")
                connection.close()
                return False

        except sqlite3.Error as e:
            print("SQLite error:", e)
            return False

    def get_current_user(self):
        return self.username

    def get_current_password(self):
        return self.password

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
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT balance
        FROM users
        WHERE user_name = ?""", (self.username,))

        bal = cursor.fetchone()
        self.balance = bal[0]
        connection.close()

        print(self.balance)
        return self.balance
