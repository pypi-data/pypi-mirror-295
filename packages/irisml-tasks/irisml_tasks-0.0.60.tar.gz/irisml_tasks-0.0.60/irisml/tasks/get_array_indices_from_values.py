from collections import defaultdict
import dataclasses
import logging
import typing
import torch

import irisml.core

logger = logging.getLogger(__name__)


# predictions -> topk indices -> get dataset ids from this task -> ICL task

class Task(irisml.core.TaskBase):
    """Go through a flat array to get indices of all items matching given values. Return a list[list[int]] in case of multiple matches.
    Support values as flat list or nested list (2-level). For nested list, concatenate all matched indices for each item in the nested list.
    flat list: e.g. array = [1, 2, 3, 3], values = [1, 3], return [[0], [2, 3]]
    nested list: e.g. array = [1, 2, 3, 3], values = [[1, 2], [3, 4], [5]], return [[0, 1], [2, 3], []].

    Inputs:
        array_list (list): List of items to search through
        array_tensor (torch.Tensor): Tensor of items to search through, must provide array_list or array_tensor
        values_list (list): List of items to search for
        values_tensor (torch.Tensor): Tensor of items to search for, must provide values_list or values_tensor
    """
    VERSION = '0.0.1'

    @dataclasses.dataclass
    class Inputs:
        array_list: typing.Optional[list] = None
        array_tensor: typing.Optional[torch.Tensor] = None
        values_list: typing.Optional[list] = None
        values_tensor: typing.Optional[torch.Tensor] = None

    @dataclasses.dataclass
    class Outputs:
        indices: list[list[int]]

    def execute(self, inputs):
        if inputs.array_tensor is not None:
            array = inputs.array_tensor.tolist()
        elif inputs.array_list is not None:
            array = inputs.array_list
        else:
            raise ValueError('Array must be provided!')
        if any(isinstance(a, list) for a in array):
            raise ValueError('Support only flat array!')

        if inputs.values_tensor is not None:
            values = inputs.values_tensor.tolist()
        elif inputs.values_list is not None:
            values = inputs.values_list
        else:
            raise ValueError('Values must be provided!')

        # Convert values to 2d list and check it is 2d
        values = [v if isinstance(v, list) else [v] for v in values]
        if any(isinstance(v2, list) for v in values for v2 in v):
            raise ValueError('Support at most 2-level nested list for values!')

        idx_by_val = defaultdict(list)
        for i, val in enumerate(array):
            idx_by_val[val].append(i)

        indices = []
        for val in values:
            val_indices = []
            for v in val:
                val_indices.extend(idx_by_val.get(v, []))
            indices.append(val_indices)

        return Task.Outputs(indices)

    def dry_run(self, inputs):
        return self.execute(inputs)
