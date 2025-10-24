from faker import Faker
fake = Faker()

# Global constants for default values
DEFAULT_MIN_CHARS = 15
DEFAULT_MAX_CHARS = 20
DEFAULT_UNIQUE_CHARS = 20
DEFAULT_MIN_INT = 100000000
DEFAULT_MAX_INT = 99999999999
DEFAULT_DELIMITER = '_'

def rand_str(min_chars = DEFAULT_MIN_CHARS, max_chars = DEFAULT_MAX_CHARS, prefix = None):
  """
  Generate a random string with specified length constraints.
  Args:
    min_chars (int): Minimum number of characters in the string
    max_chars (int): Maximum number of characters in the string
    prefix (str, optional): Prefix to prepend to the random string
  Returns:
    str: Random string with optional prefix
  """
  random_part = fake.pystr(min_chars, max_chars)
  if prefix is None:
    return random_part
  else:
    return str(prefix) + random_part

def rand_unique_str(prefix: str, delimeter=DEFAULT_DELIMITER):
  """
  Generate a unique random string with a prefix.
  Args:
    prefix (str): Prefix for the random string
    delimeter (str): Delimiter between prefix and random part
  Returns:
    str: Unique random string with prefix and delimiter
  """
  return rand_str(min_chars=DEFAULT_UNIQUE_CHARS, max_chars=DEFAULT_UNIQUE_CHARS, prefix=prefix + delimeter)

def rand_int(min=DEFAULT_MIN_INT, max=DEFAULT_MAX_INT):
  """
  Generate a random integer within specified range.
  Args:
    min (int): Minimum value for the random integer
    max (int): Maximum value for the random integer
  Returns:
    int: Random integer within the specified range
  """
  return fake.random_int(min, max)

def random_image_url():
  """
  Generate a random image URL.
  Returns:
    str: Random image URL
  """
  return fake.image_url()
