import logging
import os
from dotenv import load_dotenv

load_dotenv()

class Logger:
  _instance = None
  _logger = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Logger, cls).__new__(cls)
      cls._instance._setup_logger()
    return cls._instance

  def _setup_logger(self):
    """Setup the logger with configuration from environment variables"""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    level_mapping = {
      'DEBUG': logging.DEBUG,
      'INFO': logging.INFO,
      'WARNING': logging.WARNING,
      'ERROR': logging.ERROR,
      'CRITICAL': logging.CRITICAL
    }

    level = level_mapping.get(log_level, logging.INFO)

    self._logger = logging.getLogger('Selenium_Tests_Logger')
    self._logger.setLevel(level)

    # Clear any existing handlers to avoid duplicates
    self._logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    self._logger.addHandler(console_handler)

    # Prevent propagation to root logger
    self._logger.propagate = False

  def debug(self, message):
    """Log debug message"""
    self._logger.debug(message)

  def info(self, message):
    """Log info message"""
    self._logger.info(message)

  def warning(self, message):
    """Log warning message"""
    self._logger.warning(message)

  def error(self, message):
    """Log error message"""
    self._logger.error(message)

  def critical(self, message):
    """Log critical message"""
    self._logger.critical(message)

  def get_logger(self):
    """Get the underlying logger instance"""
    return self._logger

# Create a global logger instance
logger = Logger()
