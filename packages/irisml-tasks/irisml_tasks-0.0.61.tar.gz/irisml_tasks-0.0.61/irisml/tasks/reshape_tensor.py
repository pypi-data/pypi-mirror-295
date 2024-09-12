import dataclasses
import logging
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Reshape a tensor using the given shape.

    Config:
        shape (list[int]): The new shape. See torch.Tensor.reshape() method for the detail.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        tensor: torch.Tensor

    @dataclasses.dataclass
    class Config:
        shape: list[int]

    @dataclasses.dataclass
    class Outputs:
        tensor: torch.Tensor

    def execute(self, inputs):
        tensor = inputs.tensor.reshape(*self.config.shape)
        logger.info(f"Reshaped {inputs.tensor.shape} into {tensor.shape}")
        return self.Outputs(tensor=tensor)

    def dry_run(self, inputs):
        return self.execute(inputs)
