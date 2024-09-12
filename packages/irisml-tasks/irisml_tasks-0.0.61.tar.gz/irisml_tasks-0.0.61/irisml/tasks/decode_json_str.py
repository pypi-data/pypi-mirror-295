import dataclasses
import json
import logging
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Parse json string to dictionary.

    If parsing fails, return a dictionary, the value of which is either provided in the Config or {'failed_parse': raw_str} by default.

    Inputs:
        json_str (str): JSON string.

    Config:
        default_value (dict): In the event of a failed parse, this value is used as the parsed value. If not provided, a default dictionary {'failed_parse': raw_str} is used.

    Outputs:
        result (dict): Parsed dictionary from the input JSON string, or default_value dict when the input cannot be parsed as JSON.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        json_str: str

    @dataclasses.dataclass
    class Config:
        default_value: dict | None = None

    @dataclasses.dataclass
    class Outputs:
        result: dict

    def execute(self, inputs):
        # Remove markdown JSON block if present
        json_str = inputs.json_str.replace('```json', '').replace('```', '') if '```json' in inputs.json_str else inputs.json_str
        try:
            result = json.loads(json_str)
        except Exception as e:
            logger.info(f"Could not decode JSON string: {e}")
            result = self.config.default_value if self.config.default_value is not None else {'failed_parse': inputs.json_str}
        return self.Outputs(result=result)

    def dry_run(self, inputs):
        return self.execute(inputs)
