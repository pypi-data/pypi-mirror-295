# flake8: noqa: E501

import dataclasses
import json
import logging
from jinja2 import Template

import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Get a system prompt from the schema of a KeyValuePair dataset (https://github.com/microsoft/vision-datasets/blob/main/COCO_DATA_FORMAT.md#keyvaluepair-dataset).

    Inputs:
        schema (dict): The schema. An example for a VQA task is 
            {
                "name": "visual question answering schema",
                "description": "",
                "fieldSchema": {
                    "answer": {
                        "type": "string",
                        "description": "Answer to the question and image."
                    }
                }
            }
            More examples can be found at https://github.com/microsoft/vision-datasets/blob/main/DATA_PREPARATION.md and https://github.com/microsoft/vision-datasets/blob/main/tests/resources/util.py.

    Config:
        jinja_template: str = None. jinja template str for the system prompt which should contain three variables: schema_name, schema_description, field_schema. The will be filled with 'name',
            'description', and 'fieldSchema' from schema dictionary respectively. If jinja_template is not provided, a default template will be used.
    """
    VERSION = '0.1.1'

    TEMPLATE = '''Extract information from images in a JSON format following the provided Schema.
# Schema name{% if schema_description is not none %} and description{% endif %}
{{schema_name}}. {{schema_description}}
{% if field_schema is not none %}# JSON Schema definition
```json
{{field_schema}}
```{% endif %}
'''

    @dataclasses.dataclass
    class Inputs:
        schema: dict

    @dataclasses.dataclass
    class Config:
        jinja_template: str | None = None

    @dataclasses.dataclass
    class Outputs:
        prompt: str

    def execute(self, inputs):
        template = Template(self.config.jinja_template if self.config.jinja_template is not None else self.TEMPLATE)
        field_schema = json.dumps(inputs.schema['fieldSchema'], indent=2) if 'fieldSchema' in inputs.schema else None
        prompt = template.render(schema_name=inputs.schema['name'], schema_description=inputs.schema.get('description', ''), field_schema=field_schema)
        logger.info(f'Generated system prompt:\n{prompt}')

        return self.Outputs(prompt)

    def dry_run(self, inputs):
        return self.execute(inputs.schema)
