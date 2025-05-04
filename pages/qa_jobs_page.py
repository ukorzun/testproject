import os
import time

import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class QAJobsPage(BasePage):
    SEE_ALL_QA_JOBS = (By.LINK_TEXT, "See all QA jobs")
    LOCATION_FILTER = (By.ID, "filter-by-location")
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    JOB_LIST = (By.CSS_SELECTOR, ".position-list-item")
    POSITION_TITLE = (By.CSS_SELECTOR, "p.position-title")
    VIEW_ROLE_BUTTON = (By.LINK_TEXT, "View Role")
    QUALITY_ASSURANCE_HEADER = (By.XPATH, "//a[contains(@href, '/careers/quality-assurance/')]")
    ACCEPT_COOKIES_BUTTON = (By.ID, "wt-cli-accept-all-btn")

    @allure.step("Accept cookies by clicking 'Accept All' button")
    def accept_cookies(self):
        self.wait_and_click_element(self.ACCEPT_COOKIES_BUTTON)

    @allure.step("Open QA Careers page")
    def open_qa_page(self):
        # # self.hover_over_element(self.QUALITY_ASSURANCE_HEADER)
        # self.wait_and_click_element(self.QUALITY_ASSURANCE_HEADER)
        base_url = os.getenv("URL_UI")
        full_url = f"{base_url}/careers/quality-assurance/"
        self.driver.get(full_url)

    @allure.step("Click on 'See all QA jobs' button")
    def click_see_all_jobs(self):
        self.wait_and_click_element(self.SEE_ALL_QA_JOBS)

    @allure.step("Apply filters by clicking on custom dropdowns")
    def apply_filters(self, location, department):
        self.wait_and_click_element((By.XPATH, "//span[@id='select2-filter-by-location-container']"))
        self.wait_and_click_element((By.XPATH, f"//li[contains(text(), '{location}')]"))
        self.wait_and_click_element((By.XPATH, "//span[@id='select2-filter-by-department-container']"))
        self.wait_and_click_element((By.XPATH, f"//li[contains(text(), '{department}')]"))
        time.sleep(3)

    @allure.step("Verify that all jobs match expected Title, Department, and Location")
    def verify_job_listings(self, expected_title, expected_department, expected_location):
        self.scroll_to_element(self.JOB_LIST)
        jobs = self.wait_all_elements_in_locator(self.JOB_LIST)
        for job in jobs:
            text = job.text
            if expected_title not in text or expected_department not in text or expected_location not in text:
                return False
        return True

    @allure.step("Click 'View Role' button for position: {position_name}")
    def click_view_role_for_position(self, position_name):
        for job in self.wait_all_elements_in_locator(self.JOB_LIST):
            title = job.find_element(*self.POSITION_TITLE).text
            if position_name in title:
                button = job.find_element(*self.VIEW_ROLE_BUTTON)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                return
        assert False, f"Position '{position_name}' not found!"


    @allure.step("Select job by index {index} and click View Role")
    def select_job_by_index_and_click_view_role(self, index):
        jobs = self.wait_all_elements_in_locator((By.CSS_SELECTOR, ".position-list-item"))
        selected_job = jobs[index]

        job_title = selected_job.find_element(By.CSS_SELECTOR, "p.position-title").text
        view_role_button = selected_job.find_element(By.LINK_TEXT, "View Role")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_role_button)
        view_role_button.click()

        return job_title