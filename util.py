"""

"""
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
    pass


def find_phrase():
    """Find by a phrase"""
    pass


def quit_menu():
    """Quit menu"""
