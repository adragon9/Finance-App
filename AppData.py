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
    dat_income = None
    dat_expense_cat = None
    dat_expense_amount = None
    dat_year = None

    # Data to be used, only updated at certain points
    saved_dat_user = None
    saved_dat_pass = None
    saved_dat_income = None
    saved_dat_balance = None
    saved_dat_expense_cat = None
    saved_dat_expense_desc = None

    # Calculation variables
    calc_total_expenses = None
    calc_monthly_net = None
    calc_balance_impact = None

    # This is for saving the sessions current user
    current_user = None

    # date management
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    month_sel = None
    year_sel = None
