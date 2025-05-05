import time

import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class CareersPage(BasePage):
    SEE_ALL_TEAMS_BUTTON = (By.XPATH, "//a[contains(@class, 'loadmore') and contains(text(), 'See all teams')]")
    FIND_YOUR_CALLING_HEADER = (By.XPATH, "//h3[contains(text(), 'Find your calling')]")
    CUSTOMER_SUCCESS_HEADER = (By.XPATH, "//h3[contains(text(), 'Customer Success')]")

    @allure.step("Verify main sections and button are present on Careers Page")
    def verify_main_elements_present(self):
        self.verify_elements_visible([
            (self.SEE_ALL_TEAMS_BUTTON, "See All Teams button"),
            (self.FIND_YOUR_CALLING_HEADER, "Find Your Calling header"),
            (self.CUSTOMER_SUCCESS_HEADER, "Customer Success header"),
        ])

    @allure.step("Click on 'See all teams' button")
    def click_see_all_teams(self):
        self.scroll_to_element(self.SEE_ALL_TEAMS_BUTTON)
        time.sleep(3)
        self.wait_and_click_element(self.SEE_ALL_TEAMS_BUTTON)

    @allure.step("Verify 'Find your calling' and 'Customer Success' sections are visible after expanding teams")
    def verify_team_sections_visible(self):
        self.verify_elements_visible([
            (self.FIND_YOUR_CALLING_HEADER, "Find Your Calling header"),
            (self.CUSTOMER_SUCCESS_HEADER, "Customer Success header"),
        ])
