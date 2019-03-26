import datetime
from unittest.mock import patch
import unittest
import util
import work_log_wDB


def get_input(text):
    return input(text)


class Delete(unittest.TestCase):
    def setUp(self):
        self.entry_sample = util.Entry.create(first_name='ayman',
                                              last_name='said',
                                              task_name='test str',
                                              date=datetime.date(2019, 3, 26),
                                              time_spent=30,
                                              notes='',
                                              )

    # get_input will return 'yes' during this test
    @patch(get_input(), return_value='y')
    def test_delete_yes(self, input):
        self.assertEqual(self.entry_sample.delete_task(), True)

    @patch(get_input('nnn'), return_value='n')
    def test_delete_no(self, input):
        self.assertEqual(self.entry_sample.delete_task(), False)


class Representations(unittest.TestCase):
    def setUp(self):
        self.entry_sample = util.Entry.create(first_name='ayman',
                                              last_name='said',
                                              task_name='test str',
                                              date=datetime.date(2019, 3, 26),
                                              time_spent=30,
                                              notes='',
                                              )

    def test_str_entry_representation(self):
        expected_str = "Employee: {name}\n" \
                       "Task: {task}\n" \
                       "Date: {date}\n" \
                       "Time Spent: {time_spent}\n" \
                       "Notes: {notes}" \
                        .format(name=' '.join(['ayman'.title(),
                                               'said'.title()]),
                                task='test str',
                                date=datetime.date.strftime(
                                    datetime.date(2019, 3, 26),
                                    util.date_fmt),
                                time_spent=30,
                                notes='')
        self.assertEqual(expected_str, str(self.entry_sample))

    def test_repr_entry_representation(self):
        expected_repr = 'Entry({self.date}, ' \
               '{self.first_name}, ' \
               '{self.last_name}, ' \
               '{self.task_name},' \
               ' {self.time_spent}, ' \
               '{self.notes})'.format(self=self)
        self.assertEqual(expected_repr, repr(self.entry_sample))


if __name__ == '__main__':
    unittest.main()
