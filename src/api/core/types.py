from enum import Enum

class BaseEnum(Enum):
  pass

class HttpMethod(str, BaseEnum):
  GET = 'GET'
  POST = 'POST'
  PUT = 'PUT'
  PATCH = 'PATCH'
  DELETE = 'DELETE'
