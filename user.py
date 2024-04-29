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
        self.income = 0.0

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
            income MONEY)""")

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
            now = dt.datetime.now()
            date = now.strftime("%m-%d-%Y %H:%M:%S")

            try:
                cursor.execute("""
                INSERT INTO users(
                user_name,
                date_created,
                password,
                income) VALUES(?,?,?,?)""", (self.username, date, self.password, self.income))
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

    def create_expense_tag(self, expense_cat, expense_desc):
        status = ""
        if expense_cat.strip() == "":
            status = "You have not entered a category name!"
            return status

        if self.username != '':
            connection = sqlite3.connect('Users.db')
            cursor = connection.cursor()
            now = datetime.datetime.now()
            date = now.strftime("%m-%d-%Y %H:%M:%S")
            try:
                cursor.execute("""INSERT INTO expense_categories(
                category_name,
                user_name,
                category_date,
                category_desc) Values(?,?,?,?)""", (expense_cat, self.username, date, expense_desc))
            except sqlite3.IntegrityError:
                print("CATEGORY EXISTS")
                connection.close()
                status = "This category already exists!"
                return status

            connection.commit()
            connection.close()
            status = "Category added successfully!"
            return status
        else:
            status = "NO USER"
            return status

    def add_expense(self, expense_cat, expense_amount):
        connection = sqlite3.connect('Users.db')
        cursor = connection.cursor()
        now = datetime.datetime.now()
        date = now.strftime("%m-%d-%Y %H:%M:%S")
        status = ""
        if expense_amount.strip() == '':
            connection.close()
            status = "Expense must be greater than 0!"
            return status
        elif expense_cat.strip() == '':
            connection.close()
            status = "No category selected!"
            return status

        try:
            expense_amount = float(expense_amount)
        except ValueError:
            connection.close()
            status = "The value you have entered is not a number!"
            return status

        try:
            cursor.execute("""INSERT INTO expenses(
            category_name,
            user_name,
            expense_amount,
            expense_added) VALUES(?, ?, ?, ?)""", (expense_cat, self.username, expense_amount, date))
        except sqlite3.IntegrityError:
            print("ID EXISTS")
            connection.close()
            status = "This expense already exists!"
            return status

        connection.commit()
        connection.close()
        status = "Expense added successfully!"
        return status

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

    def set_income(self, income):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        status = ""

        try:
            self.income = float(income)
            cursor.execute("""UPDATE users
            SET income = ?
            WHERE user_name = ?""", (self.income, self.username))

            connection.commit()
            connection.close()
            status = f"Income set to: ${self.income:,.2f}"
        except ValueError:
            status = "Your input for 'income' is not a number!"

        return status

    def get_income(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT income
        FROM users
        WHERE user_name = ?""", (self.username,))

        bal = cursor.fetchone()
        self.income = bal[0]
        connection.close()

        print(self.income)
        return self.income
