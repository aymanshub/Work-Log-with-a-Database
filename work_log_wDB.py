"""
Python Web Development Techdegree
Project 3 - Work Log with a Database
--------------------------------
Developed by: Ayman Said
Mar-2019
"""
import os
from collections import OrderedDict
# import util
# import params
# from tasks import Task


def main_menu():
    """
    The startup program screen, the user is presented with
    the initial user options:
    add a new entry or lookup previous entries.
    1. Add a new entry
    2. find previous entries
    3. Quit the program
    :return: None
    """
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        welcome_msg = "Welcome To Data Based Work Log"

        print("-" * len(welcome_msg))
        print(welcome_msg)
        print("-" * len(welcome_msg))

        menu_title = "What would you like to do?"
        menu_items = ["Add new entry",
                      "Search in existing entries",
                      "Quit program",
                      ]

        menu = OrderedDict([
            ('a', add_entry),
            ('v', view_entries),
            ('s', search_entries),
        ])


        print(menu_title)
        items = enumerate(menu_items, start=1)
        for i, item in items:
            print('{}) {}'.format(i, item))
        try:
            user_input = int(input())
            if not 1 <= user_input <= len(menu_items):
                raise ValueError
        except ValueError:
            input("Invalid selection!!!, press Enter to try again...")
            continue
        else:
            if user_input == 1:
                util.add_entry()  # call add new entry function
            elif user_input == 2:
                search_menu()  # call search function
            elif user_input == 3:
                print("Quitting...Hope to see you soon!")
                return


def search_menu():
    """
    The user will be presented with the various search options that can be
    performed on the work log.
    :return: None
    """
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # clear the screen
        menu_title = "Please select your desirable search method:"
        menu_items = ["Select a Date",
                      "Range of Dates",
                      "Time spent",
                      "Exact Search",
                      "Regex Pattern",
                      ]
        previous_menu = "Return to Main menu"
        print(menu_title)
        items = enumerate(menu_items, start=1)
        for i, item in items:
            print('{}) {}'.format(i, item))
        print('[{}] {}'.format(params.previous_menu_key.upper(),
                               previous_menu))
        user_input = input()
        if user_input.upper() == params.previous_menu_key.upper():
            return  # return to Main menu
        else:
            try:
                index = int(user_input)
                if not 1 <= index <= len(menu_items):
                    raise ValueError
            except ValueError:
                input("Invalid selection!!!, press Enter to try again...")
                continue
            else:
                # loads all existing tasks in the work log CSV file
                tasks_dict = Task.load_from_log()

                if index == 1:
                    util.search_by_date(tasks_dict)
                elif index == 2:
                    util.search_range_of_dates(tasks_dict)
                elif index == 3:
                    util.search_time_spent(tasks_dict)
                elif index == 4:
                    util.search_exact_value(tasks_dict)
                elif index == 5:
                    util.search_regex_pattern(tasks_dict)


if __name__ == '__main__':
    if util.verify_log():
        main_menu()
