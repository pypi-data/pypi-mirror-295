import unittest
from irisml.tasks.decode_json_strs import Task


class TestDecodeJsonStrs(unittest.TestCase):
    def test_simple(self):
        inputs = Task.Inputs(['{"a": 1}', '{"b": 2}'])
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.dicts[0], {'a': 1})
        self.assertEqual(outputs.dicts[1], {'b': 2})

        inputs = Task.Inputs(['{"a": 1}', '{{"b": 2}'])
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.dicts[0], {'a': 1})
        self.assertEqual(outputs.dicts[1], {'failed_parse': '{{"b": 2}'})

    def test_simple_specify_default_value(self):
        inputs = Task.Inputs(['{"a": 1}', '{"b": 2}'])
        outputs = Task(Task.Config(default_value={"c": None})).execute(inputs)
        self.assertEqual(outputs.dicts[0], {'a': 1})
        self.assertEqual(outputs.dicts[1], {'b': 2})

        inputs = Task.Inputs(['{"a": 1}', '{{"b": 2}'])
        outputs = Task(Task.Config(default_value={"c": None})).execute(inputs)
        self.assertEqual(outputs.dicts[0], {'a': 1})
        self.assertEqual(outputs.dicts[1], {'c': None})

    def test_remove_json_markdown_block(self):
        inputs = Task.Inputs(['```json\n{"a": 1}   \n```'])
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.dicts[0], {'a': 1})

        inputs = Task.Inputs(['```json{"a": 1}```'])
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.dicts[0], {'a': 1})
