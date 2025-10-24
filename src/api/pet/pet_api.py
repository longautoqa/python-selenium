from src.api.core.api_client import BaseApi
from src.api.pet.types import Pet

class PetApi(BaseApi):
  PET_URI = '/pet'

  def __init__(self):
    super().__init__()

  def create_pet(self, payload: Pet, **kwargs):
    """
    Create a new pet in the system.
    Args:
      payload (Pet): Pet data containing name, status, and other attributes
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: API response object with status code and response data
    Example:
      >>> pet_data = {"name": "Buddy", "status": "available", "category": {"name": "Dogs"}}
      >>> response = pet_api.create_pet(pet_data)
      >>> print(response.status_code)
      200
    """
    return self._post(PetApi.PET_URI, json=payload, **kwargs)

  def get_pet(self, id: str, **kwargs):
    """
    Retrieve a pet by its ID.
    Args:
      id (str): Unique identifier of the pet to retrieve
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: API response object containing pet data
    Example:
      >>> response = pet_api.get_pet("123")
      >>> pet_data = response.json()
    """
    return self._get(f'{PetApi.PET_URI}/{id}', **kwargs)
  
  def update_pet(self, id: str, json=None, **kwargs):
    """
    Update an existing pet's information.
    Args:
      id (str): Unique identifier of the pet to update
      json (dict, optional): Updated pet data to send in request body
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: API response object with status code and response data
    Example:
      >>> update_data = {"name": "Buddy Updated", "status": "sold"}
      >>> response = pet_api.update_pet("123", json=update_data)
    """
    return self._put(f'{PetApi.PET_URI}/{id}', json=json, **kwargs)

  def delete_pet(self, id: int, **kwargs):
    """
    Delete a pet from the system.
    Args:
      id (int): Unique identifier of the pet to delete
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: API response object with status code
    Example:
      >>> response = pet_api.delete_pet(123)
      >>> print(response.status_code)
      200
    """
    return self._delete(f'{PetApi.PET_URI}/{id}', **kwargs)
