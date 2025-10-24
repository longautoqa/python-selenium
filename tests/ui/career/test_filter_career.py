import pytest
from src.ui.pages.home.home_page import HomePage
from src.ui.pages.core.base_page import BasePage
from src.ui.pages.career.career_page import CareerPage

class TestFilterJobs:
  # Global test data constants
  LOCATION = "Istanbul, Turkiye"
  DEPARTMENT = "Quality Assurance"
  JOBS_LEVEL_HOSTNAME = "jobs.lever.co"

  # Global test expectations
  EXPECTED_JOB_COUNT = '1'
  JOB_INDEX = 0

  @pytest.fixture(scope='function', autouse=True)
  def before_test(self, driver):
    self.base_page = BasePage(driver)
    self.home_page = HomePage(driver)
    self.career_page = CareerPage(driver)

  def test_filter_qa_jobs(self):
    """
    Test filtering QA jobs by location and department.

    This test verifies the complete flow of:
    1. Navigating to the careers page
    2. Filtering by department (Quality Assurance)
    3. Filtering by location (Istanbul, Turkiye)
    4. Verifying job records match the filters
    5. Opening a job role in a new page
    """
    self.home_page.open()
    self.home_page.verify_home_page_opened()
    self.home_page.open_careers_page()
    self.career_page.verify_careers_page_opened()
    self.career_page.verify_careers_page_blocks_displayed()
    self.career_page.navigate_to_qa_landing_page()
    self.career_page.verify_qa_landing_page_opened()
    self.career_page.click_see_all_qa_jobs()
    self.career_page.verify_qa_jobs_page_opened()
    self.career_page.verify_department_selected(self.DEPARTMENT)
    self.career_page.filter_by_location(self.LOCATION)
    self.career_page.verify_total_job_records(self.EXPECTED_JOB_COUNT)
    self.career_page.scroll_to_list_jobs()
    self.career_page.verify_job_records(self.DEPARTMENT, self.LOCATION)
    self.career_page.hover_and_click_view_role(self.JOB_INDEX)
    self.career_page.verify_job_opened_in_new_page(self.JOBS_LEVEL_HOSTNAME)
