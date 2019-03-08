"""
Python Web Development Techdegree
Project 4 - Work Log with a Database
--------------------------------
Developed by: Ayman Said
Mar-2019
"""
import os
import datetime
from collections import OrderedDict
from peewee import *

import util
# import params
# from tasks import Task

db = SqliteDatabase('work_log.db')


class Entry(Model):

    timestamp = DateTimeField(default=datetime.datetime.now, unique=True)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    time_spent = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def main_menu():
    """The startup program screen, the user is presented with
    the initial user options:
    add a new entry, search for entries or quit.
    :return: None
    """
    menu_title = "What would you like to do?"
    welcome_msg = "Welcome To Data Based Work Log"
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
    """
    The user will be presented with the various search options that can be
    performed on the work log.
    :return: None
    """
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # clear the screen
        menu_title = "Please select your desirable search method:"
        search_menu = OrderedDict([
            ('e', util.find_employee()),
            ('d', util.find_date()),
            ('r', util.find_dates_range()),
            ('t', util.find_time_spent()),
            ('p', util.find_phrase()),
            ('q', quit_menu()),

        ])


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


def quit_program():
    """Quit the program"""
    print("Quitting...Hope to see you soon!")


if __name__ == '__main__':
    initialize()
    main_menu()
