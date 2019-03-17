"""

"""
import os
import datetime
from peewee import *

db = SqliteDatabase('work_log.db')
date_fmt = '%d/%m/%Y'

class Entry(Model):
    date = DateTimeField(default=datetime.date.today, unique=False)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    time_spent = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db

    def __str__(self):
        return "Employee: {name}\n" \
               "Task: {task}\n" \
               "Date: {date}\n" \
               "Time Spent: {time_spent}\n" \
               "Notes: {notes}"\
            .format(name=self.first_name + ' ' + self.last_name,
                    task=self.task_name,
                    date=datetime.date.strftime(self.date, date_fmt),
                    time_spent=self.time_spent,
                    notes=self.notes)


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


def display_entries(entries):
    """
    Display the selected entries resulted by a user search criteria.
    :param entries: list of Task instances
    :return: None
    """
    i = 0
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        commands = "[R]eturn to search menu"
        if not len(entries):
            print("no entries have been found.".upper())
        else:
            print(entries[i])
            print("\nResult {} of {}\n".format(i + 1, len(entries)))
            commands = "[E]dit, [D]elete, " + commands
            if i < len(entries) - 1:
                # Add Next command
                commands = "[N]ext, " + commands
                if i > 0:
                    # Add Back command
                    commands = "[B]ack, " + commands
            elif i > 0:
                # Add Back command
                commands = "[B]ack, " + commands

        print(commands)
        option = input()

        if option.lower() in ['n', 'next'] and i < len(entries) - 1:
            i += 1
        elif option.lower() in ['b', 'back'] and i > 0:
            i -= 1
        elif option.lower() in ['e', 'edit'] and len(entries):
            # clear the screen
            os.system("cls" if os.name == "nt" else "clear")
            print("Please edit the following task:\n{}".format(entries[i]))
            # edit is equivalent to delete existing and make new entry
            ## entries[i].delete_task_from_log()
            ## add_new_entry(for_edit=True)
            input("editing is not implemented yet!")  # remove after
            return  # back to search menu
        elif option.lower() in ['d', 'Delete'] and len(entries):
            # call delete method
            #  entries[i].delete_task_from_log()
            input("deletion is not implemented yet!")  # remove after
            return  # back to search menu
        elif option.lower() in ['r', 'return']:
            return  # back to search menu


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
