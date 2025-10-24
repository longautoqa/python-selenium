from selenium.webdriver.common.by import By

from src.ui.pages.core.base_page import BasePage

class HomePage(BasePage):
  # Global constants for text values
  COMPANY_MENU_TEXT = "Company"
  CAREERS_LINK_TEXT = "Careers"
  FIND_YOUR_DREAM_JOB_TEXT = "Find your dream job"
  SEE_ALL_QA_JOBS_TEXT = "See all QA jobs"

  # Global constants for URLs
  DEFAULT_URL = "/"

  def __init__(self, driver) -> None:
    super().__init__(driver)

  # Locators
  __BRAND = (By.CLASS_NAME, 'navbar-brand')
  _COMPANY_MENU = (By.XPATH, f"//ul[@class='navbar-nav']//a[contains(normalize-space(text()), '{COMPANY_MENU_TEXT}')]")
  _CAREERS_LINK = (By.XPATH, f"//div[@class='new-menu-dropdown-layout-6-mid-container']//a[contains(text(), '{CAREERS_LINK_TEXT}')]")
  _FIND_YOUR_DREAM_JOB_LINK = (By.XPATH, f"//a[contains(text(), '{FIND_YOUR_DREAM_JOB_TEXT}')]")
  _SEE_ALL_QA_JOBS_LINK = (By.XPATH, f"//a[contains(text(), '{SEE_ALL_QA_JOBS_TEXT}')]")

  # Actions
  def open(self):
    """
    Navigate to the home page
    """
    self.navigate_to(self.DEFAULT_URL)

  def open_company_dropdown_menu(self):
    """
    Open the company dropdown menu by hovering over it.
    """
    self.hover_element(self._COMPANY_MENU)

  def click_careers_link(self):
    """
    Click on the careers link in the dropdown menu.
    This action should be performed after opening the company dropdown menu.
    """
    self.wait_for_click(self._CAREERS_LINK)

  # Ad-hoc functions
  def open_careers_page(self):
    """
    Navigate to the careers page through the company menu.
    This method combines multiple actions for convenience.
    """
    self.open_company_dropdown_menu()
    self.click_careers_link()

  # Assertions
  def verify_home_page_opened(self):
    """
    Check for the presence of the brand/logo element to confirm the home page is displayed.
    Raises:
      AssertionError: If the brand element is not visible
    """
    self.assert_element_visible(self.__BRAND)
