import copy
import json
import unittest
from jinja2 import Template

from irisml.tasks.get_system_prompt_from_key_value_pair_schema import Task


class TestGetSystemPromptFromKeyValuePairSchema(unittest.TestCase):
    def get_schema(self):
        return copy.deepcopy({
            "name": "UI automation Schema",
            "description": "Find UI elements and actions by natural language query from given image.",
            "fieldSchema": {
                "UIElementBox": {
                    "type": "bbox",
                    "description": "bounding box coordinates of ui element in [left, top, width, height] absolute pixel values."
                }
            }
        })

    def test_default_template(self):
        schema = self.get_schema()
        inputs = Task.Inputs(schema)
        outputs = Task(Task.Config()).execute(inputs)

        prompt = Template(Task.TEMPLATE).render(schema_name=schema['name'], schema_description=schema['description'], field_schema=json.dumps(schema['fieldSchema'], indent=2))
        self.assertEqual(outputs.prompt, prompt)

    def test_default_template_no_field_schema(self):
        schema = self.get_schema()
        del schema['fieldSchema']
        inputs = Task.Inputs(schema)
        outputs = Task(Task.Config()).execute(inputs)

        prompt = Template(Task.TEMPLATE).render(schema_name=schema['name'], schema_description=schema['description'], field_schema=None)
        self.assertEqual(outputs.prompt, prompt)

    def test_custom_template(self):
        schema = self.get_schema()
        inputs = Task.Inputs(schema)

        template = '''Write response according to schema: {{schema_name}}. {{schema_description}}\n{{field_schema}}'''
        outputs = Task(Task.Config(jinja_template=template)).execute(inputs)
        self.assertEqual(outputs.prompt, '''Write response according to schema: UI automation Schema. Find UI elements and actions by natural language query from given image.
{
  "UIElementBox": {
    "type": "bbox",
    "description": "bounding box coordinates of ui element in [left, top, width, height] absolute pixel values."
  }
}''')
