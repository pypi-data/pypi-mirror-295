import unittest
import torch
from irisml.tasks.get_array_indices_from_values import Task


class TestGetArrayIndicesFromValues(unittest.TestCase):
    def test_flat(self):
        array = [1, 2, 3, 3]
        values = [1, 2, 5]
        outputs = Task(Task.Config()).execute(Task.Inputs(array_list=array, values_list=values))
        self.assertEqual(outputs.indices, [[0], [1], []])

    def test_nested(self):
        array = [1, 2, 3, 3]
        values = [[1, 2], [3, 4], [5]]
        outputs = Task(Task.Config()).execute(Task.Inputs(array_list=array, values_list=values))
        self.assertEqual(outputs.indices, [[0, 1], [2, 3], []])

    def test_tensor(self):
        array = [1, 2, 3, 3]
        values_tensor = torch.tensor([[1, 2], [3, 4]])
        outputs = Task(Task.Config()).execute(Task.Inputs(array_list=array, values_tensor=values_tensor))
        self.assertEqual(outputs.indices, [[0, 1], [2, 3]])

        outputs = Task(Task.Config()).execute(Task.Inputs(array_tensor=torch.tensor(array), values_tensor=values_tensor))
        self.assertEqual(outputs.indices, [[0, 1], [2, 3]])

    def test_empty_array(self):
        array = []
        values = [[1, 2], [3, 4]]
        outputs = Task(Task.Config()).execute(Task.Inputs(array_list=array, values_list=values))
        self.assertEqual(outputs.indices, [[], []])
