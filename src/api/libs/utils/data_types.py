from requests import Response

def is_valid_json(response: Response):
  if not response.json():
    raise TypeError(f"Response is not a valid JSON format. Response text: {response.text}")

  return True
