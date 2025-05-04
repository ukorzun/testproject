import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class JobDetailPage(BasePage):
    POSITION_HEADER = (By.CSS_SELECTOR, 'h2')
    JOB_DESCRIPTION = (By.CSS_SELECTOR, '[data-qa="job-description"]')
    JOB_LIST = (By.CSS_SELECTOR, ".position-list-item")
    POSITION_TITLE = (By.CSS_SELECTOR, "p.position-title")
    VIEW_ROLE_BUTTON = (By.LINK_TEXT, "View Role")

    @allure.step("Get position header text")
    def get_position_header_text(self):
        return self.wait_element_to_be_visible(self.POSITION_HEADER).text

    @allure.step("Get job description text")
    def get_job_description_text(self):
        self.hover_over_element(self.POSITION_HEADER)
        return self.wait_element_to_be_visible(self.JOB_DESCRIPTION).text

    @allure.step("Find job '{expected_position_header}' and click 'View Role' after hover")
    def find_job_and_click_view_role(self, expected_position_header):
        jobs = self.wait_all_elements_in_locator(self.JOB_LIST)

        for job in jobs:
            title_element = job.find_element(*self.POSITION_TITLE)
            job_title = title_element.text.strip()

            if expected_position_header in job_title:
                self.hover_over_locator(job)

                view_role_xpath = f".//p[contains(text(), '{expected_position_header}')]/ancestor::div[contains(@class, 'position-list-item-wrapper')]//a[contains(@class, 'btn-navy')]"

                view_role_button = job.find_element(By.XPATH, view_role_xpath)

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_role_button)
                time.sleep(4)
                view_role_button.click()
