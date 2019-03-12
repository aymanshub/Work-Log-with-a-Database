"""

"""
import os
import entry


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
        entry.Entry.create(first_name=name['First'],
                           last_name=name['Last'],
                           task_name=task_name,
                           time_spent=time_spent,
                           notes=task_notes,
                           )
    except Exception as e:
        print("Error occurred while adding entry to {}\n{}"
              .format(entry.db.database, e))

    #     # create a new task instance
    # new_task = Task(date=task_date,
    #                 name=task_name,
    #                 time_spent=time_spent,
    #                 notes=task_notes)
    # my name,
    # a task name,
    # a number of minutes spent working on it,
    # and any additional notes I want to record.


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
        # display message accordingly if the work is empty
        # if not tasks_dict:
        #     print("No existing entries, work log is empty!")
        # else:
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
            #selected_tasks = []
            # select * from entry where time_spent == time_spent
            entries = entry.Entry.select()\
                                .where(entry.Entry.time_spent == time_spent)
            for i in entries:
                print(i)

            # for tasks in tasks_dict.values():
            #     for task in tasks:
            #         if task.time_spent == time_spent:
            #             selected_tasks.append(task)
            # display_tasks(selected_tasks)
            return  # go back to Search menu


def find_phrase():
    """Find by a phrase"""
    pass


def quit_menu():
    """Quit menu"""
