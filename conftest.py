import os
import pytest

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.logger import logger

def pytest_addoption(parser):
  parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")
  parser.addoption("--test-log-level", action="store", default="INFO", help="Set logging level")

@pytest.fixture(scope='session')
def browser(request):
  return request.config.getoption("--browser")

@pytest.fixture(scope='session', autouse=True)
def setup_logging(request):
  """Setup logging based on command line argument or environment variable"""
  log_level = request.config.getoption("--test-log-level")
  if log_level:
    # Set environment variable for the logger to pick up
    os.environ['LOG_LEVEL'] = log_level
    logger.info(f"Test log level set to {log_level} via command line")
  else:
    # Use environment variable or default
    env_log_level = os.getenv('LOG_LEVEL', 'INFO')
    logger.info(f"Test log level set to {env_log_level} via environment variable")

@pytest.fixture(scope='function')
def driver(browser):
  logger.info(f"Initializing {browser} driver")
  browser = browser.lower()

  if browser == 'firefox':
    logger.debug("Setting up Firefox driver")
    driver = webdriver.Firefox(service=webdriver.FirefoxService(service=webdriver.FirefoxService(GeckoDriverManager().install())))
  elif browser == 'chrome':
    logger.debug("Setting up Chrome driver")
    driver = webdriver.Chrome(service=webdriver.ChromeService(service=webdriver.ChromeService(ChromeDriverManager().install())))
  else:
    logger.error(f"Unsupported browser: {browser}")
    raise ValueError(f"Unsupported browser: {browser}")

  logger.debug("Maximizing browser window")
  driver.maximize_window()
  logger.info(f"Successfully initialized {browser} driver")

  yield driver

  logger.info("Closing browser driver")
  driver.close()
  driver.quit()
  logger.info("Browser driver closed successfully")
