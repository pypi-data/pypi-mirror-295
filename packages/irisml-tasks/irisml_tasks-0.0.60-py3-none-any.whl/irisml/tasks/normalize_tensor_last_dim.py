import dataclasses
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Normalize the last dimension of a tensor with L2 norm."""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        tensor: torch.Tensor

    @dataclasses.dataclass
    class Outputs:
        tensor: torch.Tensor

    def execute(self, inputs):
        tensor = inputs.tensor / inputs.tensor.norm(dim=-1, keepdim=True)
        return self.Outputs(tensor=tensor)

    def dry_run(self, inputs):
        return self.execute(inputs)
