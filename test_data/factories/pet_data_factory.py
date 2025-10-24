from faker import Faker
from typing import Dict, Any, Optional

from src.api.pet.types import PetStatus
from src.utils.randomize import rand_unique_str

fake = Faker()

# Global constants for pet data generation
DEFAULT_PET_ID_MIN = 10000000000000
DEFAULT_PET_ID_MAX = 9999999999999999
DEFAULT_CATEGORY_ID_MIN = 1
DEFAULT_CATEGORY_ID_MAX = 1000
DEFAULT_TAG_ID_MIN = 1
DEFAULT_TAG_ID_MAX = 1000
DEFAULT_PHOTO_URLS_COUNT = 2
DEFAULT_TAGS_COUNT = 1

def create_random_pet_body(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a random pet object with all fields populated.
  Args:
    overrides (Dict[str, Any], optional): Dictionary of field overrides
  Returns:
    Dict[str, Any]: Pet object with random data
  """
  default_payload = {
    "id": fake.random_int(min=DEFAULT_PET_ID_MIN, max=DEFAULT_PET_ID_MAX),
    "category": {
      "id": fake.random_int(min=DEFAULT_CATEGORY_ID_MIN, max=DEFAULT_CATEGORY_ID_MAX),
      "name": rand_unique_str('category')
    },
    "name": rand_unique_str('pet'),
    "photoUrls": [
      fake.image_url(),
      fake.image_url()
    ],
    "tags": [
      {
        "id": fake.random_int(min=DEFAULT_TAG_ID_MIN, max=DEFAULT_TAG_ID_MAX),
        "name": rand_unique_str('tag')
      }
    ],
    "status": PetStatus.AVAILABLE.value
  }

  # Apply overrides
  if overrides:
    default_payload.update(overrides)

  return default_payload

def update_pet_body(original: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Update an existing pet object with new values.
  Args:
    original (Dict[str, Any]): Original pet object
    overrides (Dict[str, Any], optional): Dictionary of field overrides
  Returns:
    Dict[str, Any]: Updated pet object
  """
  if overrides is None:
    return original.copy()

  result = original.copy()
  result.update(overrides)
  return result

def create_pet_with_status(status: PetStatus, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with a specific status.
  Args:
    status (PetStatus): Pet status to set
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with specified status
  """
  merged_overrides = {"status": status.value}
  if overrides:
    merged_overrides.update(overrides)

  return create_random_pet_body(merged_overrides)

def create_pet_with_photo_urls(photoUrls: list[str], overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with specific photo URLs.
  Args:
    photoUrls (list[str]): List of photo URLs
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with specified photo URLs
  """
  merged_overrides = {"photoUrls": photoUrls}
  if overrides:
    merged_overrides.update(overrides)

  return create_random_pet_body(merged_overrides)

def create_pet_with_tags(tags: Optional[str], overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with specific tags.
  Args:
    tags (Optional[str]): Tags to assign to the pet
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with specified tags
  """
  merged_overrides = {"tags": tags}
  if overrides:
    merged_overrides.update(overrides)

  return create_random_pet_body(merged_overrides)

def create_pet_with_category(category_name: str, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with a specific category.
  Args:
    category_name (str): Category name for the pet
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with specified category
  """
  merged_overrides = {"category": {"name": category_name}}
  if overrides:
    merged_overrides.update(overrides)

  return create_random_pet_body(merged_overrides)

def create_available_pet(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with 'available' status.
  Args:
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with 'available' status
  """
  return create_pet_with_status(PetStatus.AVAILABLE, overrides)

def create_pending_pet(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with 'pending' status.
  Args:
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with 'pending' status
  """
  return create_pet_with_status(PetStatus.PENDING, overrides)

def create_sold_pet(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
  """
  Create a pet object with 'sold' status.
  Args:
    overrides (Dict[str, Any], optional): Additional field overrides
  Returns:
    Dict[str, Any]: Pet object with 'sold' status
  """
  return create_pet_with_status(PetStatus.SOLD, overrides)
