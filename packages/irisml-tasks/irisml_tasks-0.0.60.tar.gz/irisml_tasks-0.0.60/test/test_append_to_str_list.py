import unittest
from irisml.tasks.append_to_str_list import Task


class TestAppendToStrList(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config()).execute(Task.Inputs(str_list=['a', 'b', 'c'], item='d'))
        self.assertEqual(outputs.str_list, ['a', 'b', 'c', 'd'])
