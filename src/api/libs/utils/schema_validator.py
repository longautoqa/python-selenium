import json
from requests import Response
from jsonschema import validate, ValidationError

class SchemaValidator:
  SCHEMA_PATH = 'src/api/libs/schemas'

  @staticmethod
  def validate_response(response: Response, file_name):
    try:
      with open(f"{SchemaValidator.SCHEMA_PATH}/{file_name}", 'r') as file:
        schema = json.load(file)
      response_data = response.json()
      validate(instance=response_data, schema=schema)

      return True
    except ValidationError as e:
      raise AssertionError(f"Schema validation failed: {e.message}")
    except Exception as e:
      raise AssertionError(f"Oops! Something went wrong: {str(e)}")
