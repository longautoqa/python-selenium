from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
from src.utils.logger import logger

load_dotenv()

TIMEOUT_IN_SECS = int(os.getenv('TIMEOUT_IN_SECS'))
BASE_URL = os.getenv('BASE_URL')

class BasePage(object):
  def __init__(self, driver) -> None:
    self._driver = driver
    self._wait = self.__init_wait()
    self._AC = ActionChains(self._driver)
    logger.debug(f"BasePage initialized with driver: {type(driver).__name__}")

  def __init_wait(self):
    """
    Initialize WebDriverWait with common exception handling.
    Returns:
      WebDriverWait: Configured wait instance with timeout and ignored exceptions
    """
    ignored_exceptions = [
      NoSuchElementException,
      ElementNotVisibleException, 
      ElementNotInteractableException, 
      StaleElementReferenceException
    ]

    return WebDriverWait(
      self._driver,
      timeout = TIMEOUT_IN_SECS,
      poll_frequency = 0.5,
      ignored_exceptions = ignored_exceptions
    )

  # Common functions
  def _wait_for_page_loaded(self):
    """
    Wait for page to be fully loaded.
    Uses JavaScript to check if the document ready state is 'complete'.
    This ensures all resources (images, stylesheets, scripts) are loaded.
    """
    self._wait.until(
      lambda driver: driver.execute_script("return document.readyState") == 'complete'
    )

  def _wait_for_element_visible(self, locator):
    """
    Wait for an element to become visible on the page.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
    Returns:
      WebElement or None: The visible element, or None if not found within timeout
    """
    logger.debug(f"Waiting for element to be visible: {locator}")
    _element = None
    try:
      _element = self._wait.until(EC.visibility_of_element_located(locator))
      logger.debug(f"Element found and visible: {locator}")
    except TimeoutException:
      logger.warning(f'Element not found with locator: {locator} within timeout {TIMEOUT_IN_SECS}s')
      print(f'Not found element with locator: {locator} within givin time, {TIMEOUT_IN_SECS}')

    return _element
  
  def _wait_for_elements_visible(self, locator):
    """
    Wait for multiple elements to become visible on the page.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
    Returns:
      list: List of visible WebElements, or empty list if none found within timeout
    """
    logger.debug(f"Waiting for multiple elements to be visible: {locator}")
    _elements = []
    try:
      _elements = self._wait.until(EC.visibility_of_all_elements_located(locator))
      logger.debug(f"Found {len(_elements)} elements: {locator}")
    except TimeoutException:
      logger.warning(f'No elements found with locator: {locator} within timeout {TIMEOUT_IN_SECS}s')
      print(f'Not found element with locator: {locator} within givin time, {TIMEOUT_IN_SECS}')

    return _elements

  def __element_to_be_clickable(self, locator):
    """
    Wait for an element to become clickable.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
    Returns:
      WebElement or None: The clickable element, or None if not clickable within timeout
    """
    _element = None
    try:
      _element = self._wait.until(EC.element_to_be_clickable(locator))
    except ElementNotVisibleException:
      print(f'Not found element with locator: {locator} within givin time, {TIMEOUT_IN_SECS}')
    except ElementNotInteractableException:
      print(f'Cannot click on: {locator}')

    return _element
  
  def wait_for_click(self, locator):
    """
    Wait for an element to be clickable and then click it.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
    Raises:
      AssertionError: If element is not found or not clickable within timeout
    """
    logger.debug(f"Attempting to click element: {locator}")
    element = self.__element_to_be_clickable(locator)
    if element is None:
      logger.error(f"Element not found or not clickable: {locator}")
      raise AssertionError(f"Element with locator {locator} not found or not clickable")
    element.click()
    logger.debug(f"Successfully clicked element: {locator}")

  def take_screenshot(self):
    """
    The screenshot is saved with a timestamp in the format: YYYY-MM-DD_at_HH-MM-SS.png
    Screenshots are saved in a 'screenshots' directory in the current working directory.
    """
    datetime_fmt = '%Y-%m-%d_at_%H-%M-%S'
    current_dt = datetime.now().strftime(datetime_fmt)
    current_dir = Path.cwd()
    screenshots_dir = Path.joinpath(current_dir, 'screenshots')
    file_name = current_dt + '.png'
    destination_file = Path.joinpath(screenshots_dir, file_name)

    try:
      self._driver.save_screenshot(destination_file)
    except:
      print('Something went wrong when trying to take a screenshot')
  
  # Common actions
  def scroll_element_into_view(self, element, behavior='smooth'):
    """
    Scroll an element into the visible area of the page.
    Args:
      element: WebElement to scroll into view
      behavior (str): Scroll behavior - 'smooth' for smooth scrolling
    """
    try:
      if behavior == 'smooth':
        self._driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth' });", element)
      else:
        self._driver.execute_script("arguments[0].scrollIntoView();", element)
    except Exception as e:
      print(f"Failed to scroll element into view: {e}")

  def hover_element(self, locator):
    """
    Hover over an element using mouse actions.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
    Returns:
      ActionChains: The performed action chain
    Raises:
      AssertionError: If element is not found or not visible
    """
    element = self._wait_for_element_visible(locator)
    if element is None:
      raise AssertionError(f"Element with locator {locator} not found for hovering")
    return self._AC.move_to_element(element).perform()

  def enter_text(self, locator, text):
    """
    Enter text into an input field.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
      text (str): Text to enter into the field
    """
    element = self._wait_for_element_visible(locator)
    element.clear()
    if text is not None:
      element.send_keys(text)

  def navigate_to(self, url):
    """
    Navigate to a URL.
    Args:
      url (str): URL to navigate to. Can be:
        - Full URL (http://diceus.com)
        - Relative path (/page)
        - Root path (/)
    """
    logger.info(f"Navigating to URL: {url}")
    url = url.lower()
    if not url.startswith(('http', 'https')):
      if url is None or url == '/':
        url = BASE_URL
      else:
        url = BASE_URL + url

    self._driver.get(url)
    logger.info(f"Successfully navigated to: {url}")

  # Common assertions
  def assert_element_visible(self, locator):
    """
    Assert that an element is visible on the page.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
    Returns:
      WebElement: The visible element
    Raises:
      AssertionError: If element is not visible within timeout
    """
    logger.debug(f"Asserting element is visible: {locator}")
    try:
      element = self._wait.until(EC.visibility_of_element_located(locator))
      logger.debug(f"Element is visible: {locator}")
      return element
    except TimeoutException:
      logger.error(f"Element not visible: {locator}")
      # self._take_screenshot(f"{element_name}_not_visible")
      raise AssertionError(f"Element with locator {locator} is not visible")
    
  def assert_text_to_be_present_in_element(self, locator, text: str):
    """
    Assert that specific text is present in an element.
    Args:
      locator (tuple): Selenium locator tuple (By, value)
      text (str): Text that should be present in the element
    Returns:
      WebElement: The element containing the text
    Raises:
      AssertionError: If text is not present within timeout
    """
    try:
      element = self._wait.until(EC.text_to_be_present_in_element(locator, text))
      return element
    except TimeoutException:
      raise AssertionError(f"Element with locator {locator} is not visible")
    
  def assert_number_of_windows(self, total: int):
    """
    Assert that the total number of browser windows/tabs matches the expected count.
    Args:
      total (int): Expected number of windows/tabs
    Raises:
      TimeoutException: If the number of windows doesn't match within timeout
    """
    self._wait.until(EC.number_of_windows_to_be(total))