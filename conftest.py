import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv
import allure

load_dotenv()

@pytest.fixture(scope="function")
def platform(request):
    return request.param

def create_driver(platform):
    if platform == "desktop_chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        if os.getenv('CI'):
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

    elif platform == "desktop_firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if os.getenv('CI'):
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unknown platform: {platform}")

    return driver

@pytest.fixture(scope="function")
def driver(request, platform):
    driver_instance = create_driver(platform)
    driver_instance.maximize_window()

    url = os.getenv('URL_UI')
    if url:
        driver_instance.get(url)
    else:
        raise ValueError("URL not set in .env")

    yield driver_instance
    driver_instance.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
