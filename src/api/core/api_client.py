import requests
from src.api.core.types import HttpMethod
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL')
TIMEOUT_IN_SECS = int(os.getenv('TIMEOUT_IN_SECS'))

class BaseApi:
  """
  Base API client class for making HTTP requests.
  Attributes:
    _base_url (str): Base URL for API endpoints
    _headers (str): Default headers for requests
  """
  def __init__(self) -> None:
    self._base_url = API_BASE_URL
    self._headers = 'Content-Type: application/json'

  def _get(self, endpoint, **kwargs):
    """
    Args:
      endpoint (str): API endpoint path (e.g., '/pets/123')
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: HTTP response object
    """
    return self.__make_request(endpoint=endpoint, method=HttpMethod.GET, **kwargs)

  def _post(self, endpoint, json=None, **kwargs):
    """
    Args:
      endpoint (str): API endpoint path (e.g., '/pets')
      json (dict, optional): JSON payload to send in request body
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: HTTP response object
    """
    return self.__make_request(endpoint=endpoint, method=HttpMethod.POST, json=json, **kwargs)

  def _put(self, endpoint, json=None, **kwargs):
    """
    Args:
      endpoint (str): API endpoint path (e.g., '/pets/123')
      json (dict, optional): JSON payload to send in request body
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: HTTP response object
    """
    return self.__make_request(endpoint=endpoint, method=HttpMethod.PUT, json=json, **kwargs)

  def _patch(self, endpoint, json=None, **kwargs):
    """
    Args:
      endpoint (str): API endpoint path (e.g., '/pets/123')
      json (dict, optional): JSON payload to send in request body
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: HTTP response object
    """
    return self.__make_request(endpoint=endpoint, method=HttpMethod.PATCH, json=json, **kwargs)

  def _delete(self, endpoint, **kwargs):
    """
    Args:
      endpoint (str): API endpoint path (e.g., '/pets/123')
      **kwargs: Additional request parameters (timeout, headers, etc.)
    Returns:
      requests.Response: HTTP response object
    """
    return self.__make_request(endpoint=endpoint, method=HttpMethod.DELETE, **kwargs)

  def __make_request(self, endpoint, method, json=None, **kwargs):
    """
    Args:
      endpoint (str): API endpoint path
      method (HttpMethod): HTTP method enum value
      json (dict, optional): JSON payload for request body
      **kwargs: Additional request parameters
    Returns:
      requests.Response: HTTP response object
    Raises:
      requests.RequestException: If the HTTP request fails
      ValueError: If an unsupported HTTP method is provided
    """
    url = self._base_url + endpoint
    timeout = dict(**kwargs).get('timeout')

    if timeout is None:
      timeout = TIMEOUT_IN_SECS

    if method == HttpMethod.GET:
      return requests.get(url=url, timeout=timeout)
    
    if method == HttpMethod.POST:
      return requests.post(url=url, json=json, timeout=timeout)

    if method == HttpMethod.PUT:
      return requests.put(url=url, json=json, timeout=timeout)

    if method == HttpMethod.PATCH:
      return requests.patch(url=url, json=json, timeout=timeout)

    if method == HttpMethod.DELETE:
      return requests.delete(url=url, json=json, timeout=timeout)
