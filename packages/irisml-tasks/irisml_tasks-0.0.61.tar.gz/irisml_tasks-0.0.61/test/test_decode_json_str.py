import unittest
from irisml.tasks.decode_json_str import Task


class TestDecodeJsonStr(unittest.TestCase):
    def test_simple(self):
        inputs = Task.Inputs('{"a": 1}')
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.result, {'a': 1})

        inputs = Task.Inputs('{{"b": 2}')
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.result, {'failed_parse': '{{"b": 2}'})

    def test_remove_json_markdown_block(self):
        inputs = Task.Inputs('```json\n{"a": 1}   \n```')
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.result, {'a': 1})

        inputs = Task.Inputs('```json{"a": 1}```')
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.result, {'a': 1})

    def test_simple_specify_default_value(self):
        inputs = Task.Inputs('{"a": 1}')
        outputs = Task(Task.Config(default_value={"c": None})).execute(inputs)
        self.assertEqual(outputs.result, {'a': 1})

        inputs = Task.Inputs('{{"b": 2}')
        outputs = Task(Task.Config(default_value={"c": None})).execute(inputs)
        self.assertEqual(outputs.result, {'c': None})
