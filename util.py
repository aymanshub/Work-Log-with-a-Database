"""

"""
import os
import datetime
from collections import namedtuple
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

    def __repr__(self):
        return 'Entry({self.date}, ' \
               '{self.first_name}, ' \
               '{self.last_name}, ' \
               '{self.task_name},' \
               ' {self.time_spent}, ' \
               '{self.notes})'.format(self=self)

    def __str__(self):
        return "Employee: {name}\n" \
               "Task: {task}\n" \
               "Date: {date}\n" \
               "Time Spent: {time_spent}\n" \
               "Notes: {notes}"\
            .format(name=' '.join([self.first_name, self.last_name]),
                    task=self.task_name,
                    date=datetime.date.strftime(self.date, date_fmt),
                    time_spent=self.time_spent,
                    notes=self.notes)

    def delete_task(self):
        """Delete an entry."""
        if input("Are you sure? [yN] ").lower() == 'y':
            self.delete_instance()
            input("Entry deleted!\nPlease press Enter to continue")
            return True
        return False

    def edit_task(self):
        """edit an entry"""
        if input("Are you sure? [yN] ").lower() == 'y':
            # clear the screen
            os.system("cls" if os.name == "nt" else "clear")
            print("Please edit the following task:\n{}".format(self))
            edited = set_entry_core_values(for_edit=True)
            self.date = edited.task_date
            self.task_name = edited.task_name
            self.time_spent = edited.time_spent
            self.notes = edited.task_notes
            self.save()
            input("Entry successfully edited!\nPlease press Enter to continue")
            return True
        return False


def set_entry_core_values(for_edit=False):

    CoreValues = namedtuple('CoreValues', [
        'task_name',
        'task_date',
        'time_spent',
        'task_notes',
        ])
    # set task name
    while True:
        task_name = input("Task name: ").strip()
        if not task_name:
            print("Please enter a meaningful task name!")
            continue
        else:
            break

    # set task date
    if for_edit:
        while True:
            # set task date
            date_input = input("Task date (please use DD/MM/YYYY format): ")
            try:
                task_date = datetime.datetime.strptime(date_input,
                                                       date_fmt).date()
            except ValueError:
                input("Invalid date!!!, press Enter to try again...")
                continue
            else:
                break
    else:
        task_date = datetime.date.today()
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

    return CoreValues(task_name, task_date, time_spent, task_notes)


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
    entry_core = set_entry_core_values()


    # # set task name
    # while True:
    #     task_name = input("Task name: ").strip()
    #     if not task_name:
    #         print("Please enter a meaningful task name!")
    #         continue
    #     else:
    #         break
    #
    # # set time_spent
    # while True:
    #     try:
    #         time_spent = int(input("Time spent (rounded minutes): "))
    #     except ValueError:
    #         input("Invalid value!!!, press Enter to try again...")
    #         continue
    #     else:
    #         break
    #
    # # set task notes
    # task_notes = input("Notes (Optional, you can leave this empty): ").strip()

    try:
        Entry.create(first_name=name['First'],
                     last_name=name['Last'],
                     task_name=entry_core.task_name,
                     date=entry_core.task_date,
                     time_spent=entry_core.time_spent,
                     notes=entry_core.task_notes,
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
            # call edit method
            if entries[i].edit_task():
                return  # back to search menu
            else:
                continue
        elif option.lower() in ['d', 'Delete'] and len(entries):
            # call delete method
            if entries[i].delete_task():
                return  # back to search menu
            else:
                continue
        elif option.lower() in ['r', 'return']:
            return  # back to search menu


def find_employee():
    """Find by employee name"""
    pass


def find_date():
    """Find by date"""
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print("From below dates list\nPlease select a date index:")
        print("Enter 'r' to Return to Search menu: ")
        dates_query = Entry\
            .select(Entry.date)\
            .distinct()\
            .order_by(Entry.date.desc())
        counter = 1
        for record in dates_query:
            print('{counter}.\t{date}'
                  .format(counter=counter, date=record.date.strftime(date_fmt)))
            counter += 1
        user_input = input()
        if user_input.upper() == 'r'.upper():
            return  # return to Search menu
        else:
            try:
                index = int(user_input)
                if 1 <= index < counter:
                    # locate records with selected index date
                    selected_date = dates_query[index-1].date
                    # entries = Entry.select() \
                    #     .where(Entry.date.cast(datetime) == selected_date)
                    entries = Entry.select().where(
                        (Entry.date.year == selected_date.year) &
                        (Entry.date.month == selected_date.month) &
                        (Entry.date.day == selected_date.day))
                else:
                    raise ValueError
            except ValueError:
                input("Invalid selection, please press Enter to try again...")
                continue
            else:
                selected_entries = []
                for entry in entries:
                    selected_entries.append(entry)
                display_entries(selected_entries)
                return  # go back to Search menu


def find_dates_range():
    """Find by dates range"""
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print("Please enter dates range, use DD/MM/YYYY format.")
        print("Enter 'r' to Return to Search menu: ")
        from_date = input("From date: ")
        if from_date.upper() == 'r'.upper():
            return  # go back to Search menu
        to_date = input("To date: ")
        if to_date.upper() == 'r'.upper():
            return  # go back to Search menu
        try:
            from_date = datetime.datetime.strptime(from_date,
                                                   date_fmt).date()
            to_date = datetime.datetime.strptime(to_date,
                                                 date_fmt).date()
        except ValueError:
            input("Invalid date!!!, press Enter to try again...")
            continue
        else:
            # locate records within the requested dates range
            entries = Entry.select().where(
                Entry.date.between(from_date,to_date))
            selected_entries = []
            for entry in entries:
                selected_entries.append(entry)
            display_entries(selected_entries)
            return  # go back to Search menu


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
            # locate records with entered time spent
            entries = Entry.select() \
                .where(Entry.time_spent == time_spent)

            for entry in entries:
                selected_entries.append(entry)
            display_entries(selected_entries)
            return  # go back to Search menu


def find_phrase():
    """Find by a phrase"""
    # clear the screen
    os.system("cls" if os.name == "nt" else "clear")
    phrase = input("Please enter a phrase to find in the Work Log:\n").strip()

    selected_entries = []
    # locate records which contains the entered phrase
    # in task_name or notes fields
    entries = Entry.select().where(
        (Entry.task_name.contains(phrase)) |
        (Entry.notes.contains(phrase)))
    for entry in entries:
        selected_entries.append(entry)
    display_entries(selected_entries)
    return  # go back to Search menu


def quit_menu():
    """Quit menu"""
