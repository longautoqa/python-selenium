from http import HTTPStatus
from requests import Response
from assertpy import assert_that

from src.api.libs.utils.data_types import is_valid_json

class Assertions:
  """
  Base assertion class provides static methods for common assertion operations
  including status code validation, data extraction, and content verification.
  """

  @staticmethod
  def __verify_status_code(response: Response, expected_code: HTTPStatus):
    """
    Verify that the response status code matches the expected code.
    Args:
      response (Response): HTTP response object
      expected_code (HTTPStatus): Expected HTTP status code
    Raises:
      AssertionError: If status codes don't match
    """
    is_valid_json(response)
    assert_that(expected_code).is_equal_to(response.status_code)

  @staticmethod
  def _find_key(response: Response, key: str):
    """
    Extract a specific key from the JSON response.
    Args:
      response (Response): HTTP response object
      key (str): Key to extract from the JSON data
    Returns:
      Any: Value associated with the key
    Raises:
      KeyError: If the key is not found in the response
    """
    data = response.json()
    if key not in data:
      raise KeyError(f"Key {key} not found in response: {data}")
    return data[key]

  @staticmethod
  def status_ok(response):
    """
    Assert that the response has a 200 OK status code.
    Args:
      response (Response): HTTP response object
    Raises:
      AssertionError: If status code is not 200
    """
    Assertions.__verify_status_code(response, HTTPStatus.OK)

  @staticmethod
  def status_not_found(actual_code: int):
    """
    Assert that the status code is 404 Not Found.
    Args:
      actual_code (int): Actual status code to verify
    Raises:
      AssertionError: If status code is not 404
    """
    assert_that(404).is_equal_to(actual_code)

  # Assertions
  @staticmethod
  def is_equal(expected_result, actual_result):
    """
    Assert that two values are equal.
    Args:
      expected_result: Expected value
      actual_result: Actual value to compare
    Raises:
      AssertionError: If values are not equal
    """
    assert_that(expected_result).is_equal_to(actual_result)

  @staticmethod
  def is_contains_key(response: Response, key: str):
    """
    Assert that the JSON response contains a specific key.
    Args:
      response (Response): HTTP response object
      key (str): Key to check for in the JSON data
    Raises:
      AssertionError: If the key is not found
    """
    assert_that(response.json()).contains_key(key)

  @staticmethod
  def contains_text(expected_text, actual_text: str):
    """
    Assert that the actual text contains the expected text.
    Args:
      expected_text: Text that should be contained
      actual_text (str): Text to search within
    Raises:
      AssertionError: If expected text is not found in actual text
    """
    assert_that(expected_text).contains(actual_text)
