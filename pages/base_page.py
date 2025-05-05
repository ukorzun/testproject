import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, platform, wait_time=50):
        self.driver = driver
        self.platform = platform
        self.wait_time = wait_time

    @allure.step("Click on element {locator}")
    def wait_and_click_element(self, locator):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable(locator)).click()

    @allure.step("Wait until element {locator} is visible")
    def wait_element_to_be_visible(self, locator):
        return WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located(locator))

    @allure.step("Wait until element {locator} is present")
    def wait_element_to_be_present(self, locator):
        return WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located(locator))

    @allure.step("Wait until all elements in locator {locator} are present")
    def wait_all_elements_in_locator(self, locator):
        return WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_all_elements_located(locator))

    @allure.step("Scroll to element {locator}")
    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Hover over element {locator}")
    def hover_over_element(self, locator):
        element = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(element).perform()

    @allure.step("Hover over given locator")
    def hover_over_locator(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    @allure.step("Verify visibility of multiple elements")
    def verify_elements_visible(self, elements: list):
        missing_elements = []
        for locator, name in elements:
            try:
                WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located(locator))
            except Exception:
                missing_elements.append(name)

        if missing_elements:
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Missing Elements",
                attachment_type=allure.attachment_type.PNG
            )
            assert False, f"The following elements are missing: {', '.join(missing_elements)}"
