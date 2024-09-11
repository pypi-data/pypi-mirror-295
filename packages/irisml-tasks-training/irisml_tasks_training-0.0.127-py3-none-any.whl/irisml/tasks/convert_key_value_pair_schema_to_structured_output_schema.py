import copy
import dataclasses
import logging
import re

import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Converts a Field Schema as defined in the vision-datasets KeyValuePair dataset schema format (https://github.com/microsoft/vision-datasets/blob/main/COCO_DATA_FORMAT.md#keyvaluepair-dataset)
    to the structured output json_schema as defined in the OpenAI structured outputs API documentation (https://platform.openai.com/docs/guides/structured-outputs/supported-schemas).

    Inputs:
        schema (dict): A vision-datasets KeyValuePair Field Schema. An example for a VQA task is
            {
                "name": "Visual question-answering schema",
                "description": "Given an image, responds with the answer to the provided question.",
                "fieldSchema": {
                    "answer": {
                        "type": "string",
                        "description": "Answer to the question given the provided image.",
                        "classes": {
                            "A": {"description": "Answer choice A."},
                            "B": {"description": ""},
                            "C": {"description": ""},
                            "D": {"description": ""}
                        }
                    }
                }
            }
            More examples can be found at https://github.com/microsoft/vision-datasets/blob/main/DATA_PREPARATION.md and https://github.com/microsoft/vision-datasets/blob/main/tests/resources/util.py.
    Outputs:
        json_schema (dict): A json_schema compatible with structured outputs in the OpenAI API. An example for the same VQA task is
            {
                "name": "Visual_question-answering_schema",
                "description": "Given an image, responds with the answer to the provided question.",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "answer": {
                            "type": "string",
                            "description": "Answer to the question given the provided image.\nFor reference, more details for a few of the possible values include:\nA: Answer choice A.",
                            "enum": ["A", "B", "C", "D"]
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "answer"
                    ]
                }
            }

    """
    VERSION = "0.1.0"

    @dataclasses.dataclass
    class Inputs:
        schema: dict

    @dataclasses.dataclass
    class Outputs:
        json_schema: dict

    def _apply_name_regex(self, name: str):
        # Apply regex to name as specified by OpenAI API: ^[a-zA-Z0-9_-]+$
        name = name.strip()
        name = re.sub(r"\s+", "_", name)
        name = re.sub(r"[^a-zA-Z0-9_-]", "", name)
        return name

    def convert_field_schema_to_structured_output_format(self, schema):
        """
        Changes on the root level:
        - Apply a regex to the "name" field.
        - Add a "strict": True field.
        - Replace 'fieldSchema' with a 'schema' field that has explicit type 'object' and move the 'fieldSchema' to 'schema' -> 'properties'.

        Changes on the key level:
        - Convert ClassSchema 'classes' keys to 'enum' format.
        - Remove includeGrounding fields.
        - Add 'additionalProperties': 'false' and 'required' list for every 'object' type.
        Details discussed in the OpenAI documentation: https://platform.openai.com/docs/guides/structured-outputs/all-fields-must-be-required.
        """
        converted = {}
        converted['name'] = self._apply_name_regex(schema['name'])
        converted['description'] = schema['description']
        converted['strict'] = True
        converted['schema'] = {}
        converted['schema']['type'] = 'object'
        converted['schema']['properties'] = copy.deepcopy(schema['fieldSchema'])

        def convert_field_schema_recursively(field_schema):
            if 'classes' in field_schema:
                field_schema['enum'] = list(field_schema['classes'].keys())

                class_descriptions = [(c, field_schema['classes'][c].get('description')) for c in field_schema['classes']]
                non_empty_class_descriptions = [f"{c}: {d}" for c, d in class_descriptions if d]
                if non_empty_class_descriptions:
                    if len(non_empty_class_descriptions) == len(field_schema['enum']):
                        description_leading_string = "For reference, more details for each of the possible values are:"
                    else:
                        description_leading_string = "For reference, more details for a few of the possible values include:"
                    # Use chr(10) to join f-string since before python 3.12, f-string expressions cannot include backslashes
                    field_schema['description'] += f"\n{description_leading_string}\n{chr(10).join(non_empty_class_descriptions)}"
                del field_schema['classes']
            if 'includeGrounding' in field_schema:
                del field_schema['includeGrounding']
            if 'items' in field_schema:
                convert_field_schema_recursively(field_schema['items'])
            if 'properties' in field_schema:
                for k in field_schema['properties'].keys():
                    convert_field_schema_recursively(field_schema['properties'][k])
                field_schema['additionalProperties'] = False
                field_schema['required'] = list(field_schema['properties'].keys())

        convert_field_schema_recursively(converted['schema'])
        logger.info(f'Converted schema to structured output format: \n{converted}')

        return converted

    def execute(self, inputs):
        json_schema = self.convert_field_schema_to_structured_output_format(inputs.schema)
        return self.Outputs(json_schema)

    def dry_run(self, inputs):
        return self.execute(inputs.schema)
