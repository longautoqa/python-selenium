from selenium.webdriver.common.by import By

from src.ui.pages.core.base_page import BasePage
from urllib.parse import urlparse

class CareerPage(BasePage):
  # Global constants for text values
  FIND_YOUR_DREAM_JOB_TEXT = "Find your dream job"
  SEE_ALL_QA_JOBS_TEXT = "See all QA jobs"
  QUALITY_ASSURANCE_TEXT = "Quality Assurance"
  ALL_OPEN_POSITIONS_TEXT = "All open positions"
  OUR_LOCATIONS_TEXT = "Our Locations"
  SEE_ALL_TEAMS_TEXT = "See all teams"
  LIFE_AT_INSIDER_TEXT = "Life at Insider"
  VIEW_ROLE_TEXT = "View Role"
  FILTER_BY_LOCATION_TEXT = "Filter by Location"
  FILTER_BY_DEPARTMENT_TEXT = "Filter by Department"
  NO_JOB_CARDS_MESSAGE = "No job cards found"

  # Global constants for URLs and paths
  QA_LANDING_PAGE_PATH = "quality-assurance"

  def __init__(self, driver) -> None:
    super().__init__(driver)

  # Locators using global constants
  _FIND_YOUR_DREAM_JOB_LINK = (By.XPATH, f"//a[contains(text(), '{FIND_YOUR_DREAM_JOB_TEXT}')]")
  _SEE_ALL_QA_JOBS_LINK = (By.XPATH, f"//a[contains(text(), '{SEE_ALL_QA_JOBS_TEXT}')]")
  _QA_LANDING_PAGE_HEADING = (By.XPATH, f"//h1[contains(text(), '{QUALITY_ASSURANCE_TEXT}')]")
  _QB_JOBS_PAGE_HEADING = (By.XPATH, f"//h3[contains(text(), '{ALL_OPEN_POSITIONS_TEXT}')]")
  _LOCATION_HEADING = (By.XPATH, f".//h3[contains(text(), '{OUR_LOCATIONS_TEXT}')]")
  _LOCATION_RESULTS_DROPDOWN = (By.XPATH, "//ul[@id='select2-filter-by-location-results']")
  _TEAM_LINK = (By.XPATH, f"//a[contains(text(), '{SEE_ALL_TEAMS_TEXT}')]")
  _LIFE_HEADING = (By.XPATH, f"//h2[contains(text(), '{LIFE_AT_INSIDER_TEXT}')]")
  _LOCATION_DROPDOWN_FIELD = (By.XPATH, "//span[@id='select2-filter-by-location-container']")
  _LIST_JOBS = (By.XPATH, "//section[@id='career-position-list']")
  _VIEW_ROLE_BUTTON = (By.XPATH, f"//a[contains(text(), '{VIEW_ROLE_TEXT}')]")
  _POSITION_DEPARTMENT = (By.XPATH, "//span[@class='position-department']")
  _POSITION_LOCATION = (By.XPATH, "//div[@class='position-location']")
  _TOTAL_RESULT = (By.XPATH, "//span[@class='totalResult']")
  _QA_JOBS_PAGE_HEADING = (By.XPATH, f"//h3[contains(text(), '{ALL_OPEN_POSITIONS_TEXT}')]")
  _FILTER_SECTION = (By.XPATH, f"//div[contains(text(), '{FILTER_BY_LOCATION_TEXT}') or contains(text(), '{FILTER_BY_DEPARTMENT_TEXT}')]")
  _DEPARTMENT_FILTER = (By.XPATH, "//span[@id='select2-filter-by-department-container']")
  _JOB_CARDS = (By.XPATH, "//div[@class='position-list-item']")

  def department_dropdown_field(self, department_text: str):
    return (By.XPATH, f"//span[@id='select2-filter-by-department-container' and text()='{department_text}']")
  
  def select_location_dropdown_field(self, location_text: str):
    return (By.XPATH, f"//li[contains(text(), '{location_text}')]")

  # Actions
  def click_see_all_qa_jobs(self):
    self.wait_for_click(self._SEE_ALL_QA_JOBS_LINK)

  # Ad-hoc functions
  def filter_by_location(self, location_name: str):
    # Open location dropdown
    self.wait_for_click(self._LOCATION_DROPDOWN_FIELD)
    # Get the dropdown element
    self._wait_for_element_visible(self._LOCATION_RESULTS_DROPDOWN)
    # Get the location option locator
    location_locator = self.select_location_dropdown_field(location_name)
    # Wait for and get the location option element
    location_option = self._wait_for_element_visible(location_locator)
    # Scroll the location option into view
    self.scroll_element_into_view(location_option)
    # Click the location option
    self.wait_for_click(location_locator)

  def scroll_to_list_jobs(self, job_index=0):
    job_cards = self._wait_for_elements_visible(self._JOB_CARDS)
    if job_cards and job_index < len(job_cards):
      self.scroll_element_into_view(job_cards[job_index])
    else:
      print(f"No job card found at index {job_index}")

  # Assertions
  def verify_careers_page_opened(self):
    self.assert_element_visible(self._FIND_YOUR_DREAM_JOB_LINK)

  def verify_careers_page_blocks_displayed(self):
    locators = [
      self._LOCATION_HEADING,
      # self._TEAM_LINK,
      # self._LIFE_HEADING
    ]

    for locator in locators:
      element = self._wait_for_element_visible(locator)
      self.scroll_element_into_view(element)

  def verify_filtered_by_department(self, department_name: str):
    self.assert_element_visible(self.department_dropdown_field(department_name))

  def verify_filtered_by_qa_department(self):
    self.verify_filtered_by_department(self.QUALITY_ASSURANCE_TEXT)

  def verify_qa_landing_page_opened(self):
    self.assert_element_visible(self._QA_LANDING_PAGE_HEADING)

  def verify_qa_jobs_page_opened(self):
    self.assert_element_visible(self._QB_JOBS_PAGE_HEADING)

  def navigate_to_qa_landing_page(self):
    self.navigate_to(f"/{self.QA_LANDING_PAGE_PATH}")

  def verify_department_selected(self, expected_department: str):
    self.assert_text_to_be_present_in_element(self._DEPARTMENT_FILTER, expected_department)

  def verify_total_job_records(self, total: int):
    # verify total result
    self.assert_text_to_be_present_in_element(self._TOTAL_RESULT, total)
    # verify total records display
    actual_records = self._wait_for_elements_visible(self._JOB_CARDS)
    actual_count = len(actual_records)

    assert actual_count == total, f"Expected {total} job records, but found {actual_count}"

  def verify_job_records(self, expected_department: str, expected_location: str):
    try:
      job_cards = self._wait_for_elements_visible(self._JOB_CARDS)
      if not job_cards:
        print(self.NO_JOB_CARDS_MESSAGE)
        return True
      print(f"Found {len(job_cards)} job records to verify")
      for i, job_card in enumerate(job_cards):
        self.scroll_element_into_view(job_card)
        try:
          position_element = job_card.find_element(*self._POSITION_LOCATION)
          position_text = position_element.text.lower()
          location_valid = expected_location.lower() in position_text
          department_valid = expected_department.lower() in position_text
          if not location_valid:
            return False
          if not department_valid:
            return False
        except Exception as e:
          return False
      return True
    except Exception as e:
      return False

  def hover_and_click_view_role(self, job_index=0):
    actual_records = self._wait_for_elements_visible(self._JOB_CARDS)
    job_card = actual_records[job_index]
    self.hover_element(job_card)
    view_role_link = job_card.find_element(*self._VIEW_ROLE_BUTTON)
    view_role_link.click()

  def verify_job_opened_in_new_page(self, expected_hostname):
    try:
      original_window = self._driver.current_window_handle
      assert len(self._driver.window_handles) == 1
      current_windows = self._driver.window_handles
      self.assert_number_of_windows(current_windows)
      # Switch to the new tab
      for window_handle in self._driver.window_handles:
        if window_handle != original_window:
          # Switch to new window
          self._driver.switch_to.new_window(window_handle)
          break
      new_url = self._driver.current_url
      # Verify the hostname
      parsed_url = urlparse(new_url)
      hostname = parsed_url.hostname
      if hostname == expected_hostname:
        return True
      else:
        return False
    except Exception as e:
      return False
