import dataclasses
import irisml.core


class Task(irisml.core.TaskBase):
    """Append a string to a list of strings.

    Inputs:
        str_list (list[str]): List of strings.
        item (str): String to append to the list.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        str_list: list[str]
        item: str

    @dataclasses.dataclass
    class Outputs:
        str_list: list[str]

    def execute(self, inputs):
        if not isinstance(inputs.str_list, list):
            raise ValueError(f'Expected str_list to be a list, got {type(inputs.str_list)}')
        if not isinstance(inputs.item, str):
            raise ValueError(f'Expected item to be a str, got {type(inputs.item)}')

        return self.Outputs(str_list=inputs.str_list + [inputs.item])

    def dry_run(self, inputs):
        return self.execute(inputs)
