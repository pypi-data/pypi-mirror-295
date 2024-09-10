import unittest
import torch
from irisml.tasks.normalize_tensor_last_dim import Task


class TestNormalizeTensorLastDim(unittest.TestCase):
    def test_simple(self):
        tensor = torch.rand((2, 3, 4))
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=tensor))

        self.assertIsInstance(outputs.tensor, torch.Tensor)
        self.assertEqual(outputs.tensor.shape, tensor.shape)
        self.assertTrue(torch.allclose(outputs.tensor.norm(dim=-1), torch.ones((2, 3))))

    def test_zero(self):
        """Test that the task doesn't crash when the input tensor is all zeros."""
        tensor = torch.zeros((2, 3, 4))
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=tensor))

        self.assertIsInstance(outputs.tensor, torch.Tensor)
        self.assertEqual(outputs.tensor.shape, tensor.shape)

    def test_scalar(self):
        tensor = torch.tensor(3.0)
        outputs = Task(Task.Config()).execute(Task.Inputs(tensor=tensor))

        self.assertIsInstance(outputs.tensor, torch.Tensor)
        self.assertEqual(outputs.tensor.shape, tensor.shape)
        self.assertAlmostEqual(outputs.tensor.item(), 1.0)
