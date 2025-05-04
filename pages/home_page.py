import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):

    COMPANY_MENU = (By.XPATH, "//a[contains(@class, 'nav-link') and contains(text(), 'Company')]")
    CAREERS_LINK = (By.XPATH, "//a[normalize-space(text())='Careers']")

    @allure.step("Navigate to Careers page")
    def navigate_to_careers(self):
        self.hover_over_element(self.COMPANY_MENU)
        self.wait_and_click_element(self.CAREERS_LINK)
