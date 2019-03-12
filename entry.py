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
