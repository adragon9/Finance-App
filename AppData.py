from dataclasses import dataclass


@dataclass
class Window:
    # Categories for the dropdown box
    dat_dropdown_categories = [""]
    dat_dropdown_choice = None
    # The current data in the entry box
    dat_user = None
    dat_password = None
    dat_balance = None
    dat_expense_cat = None
    # dat_expense_desc = None

    # Data to be used, only updated at certain points
    saved_dat_user = None
    saved_dat_pass = None
    saved_dat_balance = None
    saved_dat_expense_cat = None
    saved_dat_expense_desc = None

    # This is for saving the sessions current user
    current_user = None
