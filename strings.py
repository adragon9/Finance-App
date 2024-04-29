from dataclasses import dataclass


@dataclass
class Strings:
    title = "Finance Tracker"
    splash = "WELCOME TO THE APPLICATION"
    disclaimer = "Make sure to write down your username and password, editing has not been implemented."
    money_disclaimer = "You may manually set your income here.\nNOTE: THIS WILL OVERWRITE YOUR PREVIOUS INCOME."
    balance_desc = "Balance"
    income_desc = "Income"
    success_login = "Login successful"
    success_create_user = "User created!"
    success_create_tag = "Tag created!"
    success_add_expense = "Expense added!"
    success_balance = "You successfully set your income to: "
    fail_login = "Match not found login failed"
    fail_balance = "Your income input was not valid income is: "
    fail_create_user = "User already exists or some other error has occurred user not created."
    fail_create_tag = "Tag already exists or an error has occurred!"
    fail_add_expense = "A problem has occurred expense not added!"
    blank = "Entry boxes not filled out"
    username = "Username"
    password = "Password"
    cat = "Category Name"
    cat_desc = "Category Description"
    expense_category_desc = "Here you can create categories for your expense (example: Subscriptions, Groceries, etc.)"
    placeholder = "placeholder"
