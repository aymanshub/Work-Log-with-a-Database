"""
The unit-tests used for the work log Database program.
note: running the tests will empty the DB table.
"""
import datetime
from unittest import mock
import unittest
import util
import work_log_wDB

date_fmt = '%d/%m/%Y'


class EditDelete(unittest.TestCase):
    def setUp(self):
        work_log_wDB.initialize()
        self.entry_sample = util.Entry.create(first_name='ayman',
                                              last_name='said',
                                              task_name='test Delete',
                                              date=datetime.date(2019, 3, 26),
                                              time_spent=30,
                                              notes='',
                                              )

    def tearDown(self):
        try:
            util.Entry.delete().execute()
        except Exception as e:
            print("Error occurred during tear down of {}\n{}"
                  .format(self.__class__, e))
        util.db.close()

    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'set_entry_core_values', autospec=True)
    @mock.patch.object(util.Entry, 'save')
    def test_edit(self, mock_save, mock_set_entry_core_values, mock_print):
        # simulating the user input upon the deletion request
        with mock.patch('builtins.input', return_value="n"):
            result = self.entry_sample.edit_task()
            mock_save.assert_not_called()
            self.assertEqual(result, False)
        with mock.patch('builtins.input', return_value="y"):
            result = self.entry_sample.edit_task()
            mock_set_entry_core_values.assert_called_once_with(for_edit=True)
            mock_save.assert_called_once()
            self.assertEqual(result, True)

    @mock.patch.object(util.Entry, 'delete_instance')
    def test_delete(self, mock_method):
        # simulating the user input upon the deletion request
        with mock.patch('builtins.input', return_value="n"):
            self.entry_sample.delete_task()
            mock_method.assert_not_called()
            self.assertEqual(self.entry_sample.delete_task(), False)
        with mock.patch('builtins.input', return_value="y"):
            self.entry_sample.delete_task()
            mock_method.assert_called_once()
            self.assertEqual(self.entry_sample.delete_task(), True)


class Representations(unittest.TestCase):
    def setUp(self):
        work_log_wDB.initialize()
        self.entry_sample = util.Entry.create(first_name='ayman',
                                              last_name='said',
                                              task_name='test str',
                                              date=datetime.date(2019, 3, 26),
                                              time_spent=30,
                                              notes='',
                                              )

    def tearDown(self):
        try:
            util.Entry.delete().execute()
        except Exception as e:
            print("Error occurred during tear down of {}\n{}"
                  .format(self.__class__, e))
        util.db.close()

    @mock.patch('os.system', autospec=True)
    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util.Entry, 'edit_task', autospec=False)
    @mock.patch.object(util.Entry, 'delete_task', autospec=False)
    def test_display_entries(self, mock_delete_task, mock_edit_task,
                             mock_print, mock_os):
        # no entries to display
        entries = []
        with mock.patch('builtins.input', return_value="r"):
            result = util.display_entries(entries)
            mock_edit_task.assert_not_called()
            mock_delete_task.assert_not_called()
            self.assertEqual(result, True)
        # one entry to display
        entries = [self.entry_sample]
        with mock.patch('builtins.input', return_value="e"):
            result = util.display_entries(entries)
            mock_edit_task.assert_called_once_with()
            mock_delete_task.assert_not_called()
            self.assertEqual(result, True)
        mock_edit_task.reset_mock()
        mock_delete_task.reset_mock()
        with mock.patch('builtins.input', return_value="d"):
            result = util.display_entries(entries)
            mock_edit_task.assert_not_called()
            mock_delete_task.assert_called_once_with()
            self.assertEqual(result, True)
        # two entries to display
        entries.append(self.entry_sample)
        mock_edit_task.reset_mock()
        mock_delete_task.reset_mock()
        with mock.patch('builtins.input', side_effect=["n", "b", "r"]):
            result = util.display_entries(entries)
            self.assertEqual(2, len(entries))
            self.assertEqual(result, True)
            mock_edit_task.assert_not_called()
            mock_delete_task.assert_not_called()

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
               '{self.notes})'.format(self=self.entry_sample)
        self.assertEqual(expected_repr, repr(self.entry_sample))


class Menus(unittest.TestCase):
    @mock.patch('os.system', autospec=True)
    @mock.patch('builtins.print', autospec=False)
    @mock.patch.object(util, 'add_entry', autospec=True)
    @mock.patch.object(work_log_wDB, 'search_entries', autospec=True)
    @mock.patch.object(work_log_wDB, 'quit_program', autospec=True)
    def test_main_menu(self,
                       mock_quit_program,
                       mock_search_entries,
                       mock_add_entry,
                       mock_print,
                       mock_os,
                       ):
        with mock.patch('builtins.input', side_effect=["a", "s", "q"]):
            work_log_wDB.main_menu()
            mock_add_entry.assert_called_once_with()
            mock_search_entries.assert_called_once_with()
            mock_quit_program.assert_called_once_with()

    @mock.patch('os.system', autospec=True)
    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'quit_menu', autospec=True)
    @mock.patch.object(util, 'find_phrase', autospec=True)
    @mock.patch.object(util, 'find_time_spent', autospec=True)
    @mock.patch.object(util, 'find_dates_range', autospec=True)
    @mock.patch.object(util, 'find_date', autospec=True)
    @mock.patch.object(util, 'find_employee', autospec=True)
    def test_search_entries(self,
                            mock_find_employee,
                            mock_find_date,
                            mock_find_dates_range,
                            mock_find_time_spent,
                            mock_find_phrase,
                            mock_quit_menu,
                            mock_print,
                            mock_os,
                            ):
        with mock.patch('builtins.input',
                        side_effect=["e", "d", "r", "t", "p", "q"]):
            work_log_wDB.search_entries()
            mock_find_employee.assert_called_once_with()
            mock_find_date.assert_called_once_with()
            mock_find_dates_range.assert_called_once_with()
            mock_find_time_spent.assert_called_once_with()
            mock_find_phrase.assert_called_once_with()
            mock_quit_menu.assert_called_once_with()


class SearchMethods(unittest.TestCase):
    def setUp(self):
        work_log_wDB.initialize()
        self.entry_sample = util.Entry.create(first_name='ayman',
                                              last_name='said',
                                              task_name='test str',
                                              date=datetime.date(2019, 3, 26),
                                              time_spent=30,
                                              notes='can you find this?',
                                              )

    def tearDown(self):
        try:
            util.Entry.delete().execute()
        except Exception as e:
            print("Error occurred during tear down of {}\n{}"
                  .format(self.__class__, e))
        util.db.close()

    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_find_phrase(self, mock_display_entries):
        with mock.patch('builtins.input', return_value="can"):
            result = util.find_phrase()
            self.assertEqual(1, result)
            mock_display_entries.assert_called_once()

    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_find_time_spent(self, mock_display_entries, mock_print):
        with mock.patch('builtins.input', return_value="30"):
            result = util.find_time_spent()
            self.assertEqual(1, result)
            mock_display_entries.assert_called_once()

    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_find_date(self, mock_display_entries, mock_print):
        with mock.patch('builtins.input', return_value="1"):
            result = util.find_date()
            self.assertEqual(1, result)
            mock_display_entries.assert_called_once()

    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_find_date_with_emptyDB(self, mock_display_entries, mock_print):
        with mock.patch('builtins.input', return_value="r"):
            self.entry_sample.delete_instance()
            result = util.find_date()
            self.assertEqual(result, True)
            mock_display_entries.assert_not_called()

    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_find_employee(self, mock_display_entries, mock_print):
        with mock.patch('builtins.input', return_value="ayman said"):
            result = util.find_employee()
            self.assertEqual(1, result)
            mock_display_entries.assert_called_once()

    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_look_for_partners(self, mock_display_entries, mock_print):
        with mock.patch('builtins.input', return_value="1"):
            entries = util.look_for_partners("ayman")
            self.assertEqual(1, len(entries))
            mock_display_entries.assert_not_called()

    @mock.patch('builtins.print', autospec=True)
    def test_invalid_look_for_partners(self, mock_print):
            entries = util.look_for_partners("George")
            self.assertEqual(None, entries)

    # find_dates_range
    @mock.patch('builtins.print', autospec=True)
    @mock.patch.object(util, 'display_entries', autospec=True)
    def test_find_dates_range(self, mock_display_entries, mock_print):
        with mock.patch('builtins.input',
                        side_effect=['26/3/2019', '30/3/2019']):
            result = util.find_dates_range()
            self.assertEqual(1, result)
            mock_display_entries.assert_called_once()


class AddEntry(unittest.TestCase):
    def setUp(self):
        work_log_wDB.initialize()
        self.entry_sample = util.Entry.create(first_name='ayman',
                                              last_name='said',
                                              task_name='test str',
                                              date=datetime.date(2019, 3, 26),
                                              time_spent=30,
                                              notes='can you find this?',
                                              )

    def tearDown(self):
        try:
            util.Entry.delete().execute()
        except Exception as e:
            print("Error occurred during tear down of {}\n{}"
                  .format(self.__class__, e))
        util.db.close()

    @mock.patch.object(util, 'set_entry_core_values', autospec=False)
    @mock.patch.object(util.Entry, 'create', autospec=False)
    def test_add_entry(self, mock_create, mock_set_entry_core_values):
        with mock.patch('builtins.input', return_value='Lina Said'):
                result = util.add_entry()
                self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
