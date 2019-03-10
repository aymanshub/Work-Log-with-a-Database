"""
Python Web Development Techdegree
Project 4 - Work Log with a Database
--------------------------------
Developed by: Ayman Said
Mar-2019
"""
import os

from collections import OrderedDict
import entry
import util

# import params
# from tasks import Task


def initialize():
    """Create the database and the table if they don't exist."""
    entry.db.connect()
    entry.db.create_tables([entry.Entry], safe=True)


def main_menu():
    """The startup program screen, the user is presented with
    the initial user options:
    add a new entry, search for entries or quit.
    :return: None
    """
    menu_title = "What would you like to do?"
    welcome_msg = "Data Based Work Log"
    # An OrderedDict representing the main menu items & their functions
    menu = OrderedDict([
        ('a', util.add_entry),
        ('s', search_entries),
        ('q', quit_program),
    ])

    choice = None
    while choice != 'q':
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print("-" * len(welcome_msg))
        print(welcome_msg)
        print("-" * len(welcome_msg))
        print(menu_title)
        for key, value in menu.items():
            # using the function docstring as the menu items
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        if choice in menu:
            menu[choice]()
        else:
            input("Invalid selection!!!, press Enter to try again...")
            continue


def search_entries():
    """Search for entries"""
    menu_title = "Please select your desirable search method:"
    search_menu = OrderedDict([
        ('e', util.find_employee),
        ('d', util.find_date),
        ('r', util.find_dates_range),
        ('t', util.find_time_spent),
        ('p', util.find_phrase),
        ('q', util.quit_menu),

    ])

    choice = None
    while choice != 'q':
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print(menu_title)
        for key, value in search_menu.items():
            # using the function docstring as the menu items
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        if choice in search_menu:
            search_menu[choice]()
        else:
            input("Invalid selection!!!, press Enter to try again...")
            continue


def quit_program():
    """Quit the program"""
    print("Quitting...Hope to see you soon!")


if __name__ == '__main__':
    initialize()
    main_menu()
