import dataclasses
import json
import logging
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Parse a list of json strings to dictionaries.

    If parsing fails, return a dictionary, the value of which is either provided in the Config or {'failed_parse': raw_str} by default.

    Inputs:
        json_strs (List[str]): JSON strings.

    Config:
        default_value (dict): In the event of a failed parse, this value is used as the parsed value. If not provided, a default dictionary {'failed_parse': raw_str} is used.

    Outputs:
        dicts (List[dict]): Parsed dictionaries from the input JSON strings, or default_value dicts when the input cannot be parsed as JSON.
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Inputs:
        json_strs: list[str]

    @dataclasses.dataclass
    class Config:
        default_value: dict | None = None

    @dataclasses.dataclass
    class Outputs:
        dicts: list[dict]

    def execute(self, inputs):
        dicts = []
        for json_str in inputs.json_strs:
            # Remove markdown json block if present
            json_str = json_str.replace('```json', '').replace('```', '') if '```json' in json_str else json_str
            try:
                dicts.append(json.loads(json_str))
            except Exception as e:
                logger.info(f"Could not decode JSON string: {e}")
                dicts.append(self.config.default_value if self.config.default_value is not None else {'failed_parse': json_str})
        return self.Outputs(dicts=dicts)

    def dry_run(self, inputs):
        return self.execute(inputs)
