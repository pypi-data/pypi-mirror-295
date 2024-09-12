import unittest
import torch
from irisml.tasks.reshape_tensor import Task


class TestReshapeTensor(unittest.TestCase):
    def test_simple(self):
        tensor = torch.rand((2, 3, 4))
        outputs = Task(Task.Config(shape=[2, 3, 2, 2])).execute(Task.Inputs(tensor))
        self.assertEqual(outputs.tensor.shape, (2, 3, 2, 2))
        self.assertTrue(torch.equal(outputs.tensor, tensor.reshape(2, 3, 2, 2)))

    def test_variable(self):
        tensor = torch.rand((2, 3, 4))
        outputs = Task(Task.Config(shape=[-1, 1, 4])).execute(Task.Inputs(tensor))
        self.assertEqual(outputs.tensor.shape, (6, 1, 4))
        self.assertTrue(torch.equal(outputs.tensor, tensor.reshape(6, 1, 4)))

    def test_failure(self):
        tensor = torch.rand((2, 3, 4))
        with self.assertRaises(RuntimeError):
            Task(Task.Config(shape=[3, 3, 4])).execute(Task.Inputs(tensor))
