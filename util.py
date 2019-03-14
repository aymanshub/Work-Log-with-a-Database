"""

"""
import os
import datetime
from peewee import *

db = SqliteDatabase('work_log.db')


class Entry(Model):
    date = DateTimeField(default=datetime.date.today, unique=False)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    time_spent = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db


def add_entry():
    """Add a new entry"""

    # set employee name
    name = {'First': None,
            'Last': None,
            }
    for key in name.keys():
        while True:
            name[key] = input(key + " name: ").strip()
            if not name[key]:
                print("Please enter a meaningful name!")
                continue
            else:
                break

    # set task name
    while True:
        task_name = input("Task name: ").strip()
        if not task_name:
            print("Please enter a meaningful task name!")
            continue
        else:
            break

    # set time_spent
    while True:
        try:
            time_spent = int(input("Time spent (rounded minutes): "))
        except ValueError:
            input("Invalid value!!!, press Enter to try again...")
            continue
        else:
            break

    # set task notes
    task_notes = input("Notes (Optional, you can leave this empty): ").strip()

    try:
        Entry.create(first_name=name['First'],
                     last_name=name['Last'],
                     task_name=task_name,
                     time_spent=time_spent,
                     notes=task_notes,
                     )
    except Exception as e:
        print("Error occurred while adding entry to {}\n{}"
              .format(db.database, e))


def display_entries(elist):
    pass


def find_employee():
    """Find by employee name"""
    pass


def find_date():
    """Find by date"""
    pass


def find_dates_range():
    """Find by dates range"""
    pass


def find_time_spent():
    """Find by time spent"""
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print("Please enter a time spent value (rounded minutes)")
        print("Enter 'r' to Return to Search menu: ")

        time_spent = input()

        if time_spent.upper() == 'r'.upper():
            return  # go back to Search menu
        try:
            time_spent = int(time_spent)
        except ValueError:
            input("Invalid value!!!, press Enter to try again...")
            continue
        else:
            selected_entries = []
            entries = Entry.select() \
                .where(Entry.time_spent == time_spent)

            for entry in entries:
                selected_entries.append(entry)
            display_entries(selected_entries)
            return  # go back to Search menu


def find_phrase():
    """Find by a phrase"""
    pass


def quit_menu():
    """Quit menu"""
