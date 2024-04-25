from dataclasses import dataclass


@dataclass
class Strings:
    title = "Finance Tracker"
    splash = "WELCOME TO THE APPLICATION"
    disclaimer = "Make sure to write down your username and password, editing has not been implemented."
    balance_desc = "You may manually set your balance here.\nNOTE: THIS WILL OVERWRITE YOUR PREVIOUS BALANCE."
    success_create = "User created!"
    fail_login = "Match not found login failed"
    success = "Login successful"
    blank = "Entry boxes not filled out"
    success_balance = "You successfully set your balance too: "
    fail_balance = "Your balance input was not valid balance set to: "
    fail_create = "User already exists or some other error has occurred user not created."
    username = "Username"
    password = "Password"
    cat = "Category Name"
    cat_desc = "Category Description"
    expense_category_desc = "Here you can create categories for your expense (example: Subscriptions, Groceries, etc.)"
