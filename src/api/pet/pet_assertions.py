"""
Pet-specific assertion utilities for API testing.

This module provides assertion methods specifically for validating
pet-related API responses and data extraction.
"""

from requests import Response
from src.api.libs.utils.assertions import Assertions

class PetAssertions(Assertions):
  @staticmethod
  def get_pet_status(response: Response) -> str:
    """
    Extract the status field from a pet API response.
    Args:
      response (Response): HTTP response object containing pet data
    Returns:
      str: Pet status value
    """
    return PetAssertions._find_key(response, 'status')

  @staticmethod
  def get_photo_urls(response: Response) -> str:
    """
    Extract the photoUrls field from a pet API response.
    Args:
      response (Response): HTTP response object containing pet data
    Returns:
      str: List of photo URLs
    """
    return PetAssertions._find_key(response, 'photoUrls')

  @staticmethod
  def get_pet_tags(response: Response) -> str:
    """
    Extract the tags field from a pet API response.
    Args:
      response (Response): HTTP response object containing pet data
    Returns:
      str: List of pet tags
    """
    return PetAssertions._find_key(response, 'tags')

  @staticmethod
  def get_pet_id(response: Response) -> int:
    """
    Extract the ID field from a pet API response.
    Args:
      response (Response): HTTP response object containing pet data
    Returns:
      int: Pet ID
    """
    return PetAssertions._find_key(response, 'id')

  @staticmethod
  def get_pet_name(response: Response) -> str:
    """
    Extract the name field from a pet API response.
    Args:
      response (Response): HTTP response object containing pet data
    Returns:
      str: Pet name
    """
    return PetAssertions._find_key(response, 'name')
  
  @staticmethod
  def extract_tag_names(response: Response):
    """
    Extract tag names from the tags array in a pet response.
    Args:
      response (Response): HTTP response object containing pet data
    Returns:
      list: List of tag names
    """
    tags = response.json()['tags']
    return [tag['name'] for tag in tags] if tags else []

  @staticmethod
  def assert_pet_status(response: Response, expected_status: str):
    """
    Assert that the pet status matches the expected value.
    Args:
      response (Response): HTTP response object containing pet data
      expected_status (str): Expected pet status
    Raises:
      AssertionError: If status doesn't match
    """
    actual_status = PetAssertions.get_pet_status(response)
    Assertions.is_equal(expected_status, actual_status)

  @staticmethod
  def assert_pet_tag_names(response: Response, expected_tags: list[str]):
    """
    Assert that the pet tag names match the expected values.
    Args:
      response (Response): HTTP response object containing pet data
      expected_tags (list[str]): Expected list of tag names
    Raises:
      AssertionError: If tag names don't match
    """
    actual_tags = PetAssertions.extract_tag_names(response)
    Assertions.is_equal(expected_tags, actual_tags)

  @staticmethod
  def assert_pet_photo_urls(response: Response, expected_photos: list[str]):
    """
    Assert that the pet photo URLs match the expected values.
    Args:
      response (Response): HTTP response object containing pet data
      expected_photos (list[str]): Expected list of photo URLs
    Raises:
      AssertionError: If photo URLs don't match
    """
    actual_photos = PetAssertions.get_photo_urls(response)
    Assertions.is_equal(expected_photos, actual_photos)

  @staticmethod
  def assert_pet_created_successfully(response: Response):
    """
    Assert that a pet was created successfully.
    This method verifies:
    - Response status is 200 OK
    - Response contains an 'id' field
    Args:
      response (Response): HTTP response object from pet creation
    Raises:
      AssertionError: If creation was not successful
    """
    Assertions.status_ok(response)
    Assertions.is_contains_key(response, key='id')
