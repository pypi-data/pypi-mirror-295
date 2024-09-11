import copy
import unittest
from irisml.tasks.convert_key_value_pair_schema_to_structured_output_schema import Task


class TestConvertKeyValuePairSchemaToStructuredOutputSchema(unittest.TestCase):
    def test_simple_schema(self):
        schema = {
            "name": "Simple Schema",
            "description": "A simple schema with only root keys.",
            "fieldSchema": {
                "image_description": {
                    "type": "string",
                    "description": "Description of the image in a few sentences, with attention to detail."
                },
                "number_of_chinchillas": {
                    "type": "integer",
                    "description": "Number of chinchillas visible in the image."
                },
                "activity": {
                    "type": "string",
                    "description": "The most salient activity of the chinchillas in the image.",
                    "classes": {
                        "sleeping": {"description": "Often in a supine position."},
                        "running": {"description": ""},
                        "eating": {"description": "Consuming solid foods."}
                    }
                }
            }
        }
        expected_output = {
            "name": "Simple_Schema",
            "description": "A simple schema with only root keys.",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "image_description": {
                        "type": "string",
                        "description": "Description of the image in a few sentences, with attention to detail."
                    },
                    "number_of_chinchillas": {
                        "type": "integer",
                        "description": "Number of chinchillas visible in the image."
                    },
                    "activity": {
                        "type": "string",
                        "description": "The most salient activity of the chinchillas in the image.\n"
                        "For reference, more details for a few of the possible values include:\nsleeping: Often in a supine position.\neating: Consuming solid foods.",
                        "enum": ["sleeping", "running", "eating"]
                    }
                },
                "additionalProperties": False,
                "required": [
                    "image_description", "number_of_chinchillas", "activity"
                ]
            }
        }
        schema_before_execution = copy.deepcopy(schema)
        outputs = Task(Task.Config()).execute(Task.Inputs(schema=schema))
        self.assertEqual(outputs.json_schema, expected_output)
        self.assertEqual(schema, schema_before_execution)

    def test_simple_list_schema(self):
        schema = {
            "name": "defect detection",
            "description": "detect the defects in the image",
            "fieldSchema": {
                "defects": {
                    "type": "array",
                    "description": "The defect types present in the image.",
                    "items": {
                        "type": "string",
                        "description": "The type of defect detected",
                        "classes": {
                            "scratch": {},
                            "dent": {},
                            "discoloration": {},
                            "crack": {}
                        },
                        "includeGrounding": True
                    }
                }
            }
        }
        expected_output = {
            "name": "defect_detection",
            "description": "detect the defects in the image",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "defects": {
                        "type": "array",
                        "description": "The defect types present in the image.",
                        "items": {
                            "type": "string",
                            "description": "The type of defect detected",
                            "enum": ["scratch", "dent", "discoloration", "crack"]
                        }
                    }
                },
                "additionalProperties": False,
                "required": [
                    "defects"
                ]
            }
        }
        schema_before_execution = copy.deepcopy(schema)
        outputs = Task(Task.Config()).execute(Task.Inputs(schema=schema))
        self.assertEqual(outputs.json_schema, expected_output)
        self.assertEqual(schema, schema_before_execution)

    def test_complex_list_schema_invalid_name_char(self):
        schema = {
            "name": "Defect detection!",
            "description": "Detect the defects!",
            "fieldSchema": {
                "defects": {
                    "type": "array",
                    "description": "The defect types present in the image.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "defect_type": {
                                "type": "string",
                                "description": "The type of defect detected",
                                "classes": {
                                    "scratch": {},
                                    "dent": {},
                                    "discoloration": {},
                                    "crack": {}
                                },
                                "includeGrounding": True
                            },
                            "explanation": {
                                "type": "string",
                                "description": "Rationale for the defects identified."
                            }
                        }
                    }
                }
            }
        }
        expected_output = {
            "name": "Defect_detection",
            "description": "Detect the defects!",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "defects": {
                        "type": "array",
                        "description": "The defect types present in the image.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "defect_type": {
                                    "type": "string",
                                    "description": "The type of defect detected",
                                    "enum": ["scratch", "dent", "discoloration", "crack"]
                                },
                                "explanation": {
                                    "type": "string",
                                    "description": "Rationale for the defects identified."
                                }
                            },
                            "additionalProperties": False,
                            "required": [
                                "defect_type", "explanation"
                            ]
                        }
                    }
                },
                "additionalProperties": False,
                "required": [
                    "defects"
                ]
            }
        }
        schema_before_execution = copy.deepcopy(schema)
        outputs = Task(Task.Config()).execute(Task.Inputs(schema=schema))
        self.assertEqual(outputs.json_schema, expected_output)
        self.assertEqual(schema, schema_before_execution)

    def test_nested_object_schema(self):
        schema = {
            "name": "Brand sentiment identification",
            "description": "Identify various attributes pertaining to brand sentiment.",
            "fieldSchema": {
                "brand_sentiment": {
                    "type": "object",
                    "description": "Attributes of sentiment toward brands depicted in the image.",
                    "properties": {
                        "has_non_contoso_brands": {
                            "type": "boolean",
                            "description": "Whether the image depicts or contains anything about non-Contoso brands."
                        },
                        "contoso_specific": {
                            "type": "object",
                            "description": "Sentiment related specifically to the company Contoso.",
                            "properties": {
                                "sentiment": {
                                    "type": "string",
                                    "description": "Sentiment toward the brand as depicted in the image.",
                                    "classes": {
                                        "very positive": {"description": "The highest possible positivity"},
                                        "somewhat positive": {},
                                        "neutral": {},
                                        "somewhat negative": {},
                                        "very negative": {"description": "The lowest possible positivity"}
                                    }
                                },
                                "logos": {
                                    "type": "array",
                                    "description": "The types of Contoso logos present in the image.",
                                    "items": {
                                        "type": "string",
                                        "description": "The type of Contoso logo in the image.",
                                        "classes": {
                                            "text": {"description": "The text-only logo"},
                                            "grayscale": {"description": "The grayscale logo"},
                                            "rgb": {"description": "The full-color logo"}
                                        },
                                        "includeGrounding": True
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        expected_output = {
            "name": "Brand_sentiment_identification",
            "description": "Identify various attributes pertaining to brand sentiment.",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "brand_sentiment": {
                        "type": "object",
                        "description": "Attributes of sentiment toward brands depicted in the image.",
                        "properties": {
                            "has_non_contoso_brands": {
                                "type": "boolean",
                                "description": "Whether the image depicts or contains anything about non-Contoso brands."
                            },
                            "contoso_specific": {
                                "type": "object",
                                "description": "Sentiment related specifically to the company Contoso.",
                                "properties": {
                                    "sentiment": {
                                        "type": "string",
                                        "description": "Sentiment toward the brand as depicted in the image.\n"
                                        "For reference, more details for a few of the possible values include:\nvery positive: The highest possible positivity\n"
                                        "very negative: The lowest possible positivity",
                                        "enum": ["very positive", "somewhat positive", "neutral", "somewhat negative", "very negative"]
                                    },
                                    "logos": {
                                        "type": "array",
                                        "description": "The types of Contoso logos present in the image.",
                                        "items": {
                                            "type": "string",
                                            "description": "The type of Contoso logo in the image.\n"
                                            "For reference, more details for each of the possible values are:\n"
                                            "text: The text-only logo\ngrayscale: The grayscale logo\nrgb: The full-color logo",
                                            "enum": ["text", "grayscale", "rgb"]
                                        }
                                    }
                                },
                                "additionalProperties": False,
                                "required": [
                                    "sentiment", "logos"
                                ]
                            }
                        },
                        "additionalProperties": False,
                        "required": [
                            "has_non_contoso_brands", "contoso_specific"
                        ]
                    }
                },
                "additionalProperties": False,
                "required": [
                    "brand_sentiment"
                ]
            }
        }
        schema_before_execution = copy.deepcopy(schema)
        outputs = Task(Task.Config()).execute(Task.Inputs(schema=schema))
        self.assertEqual(outputs.json_schema, expected_output)
        self.assertEqual(schema, schema_before_execution)
