import time
import pytest
import allure
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.job_details_page import JobDetailPage
from pages.qa_jobs_page import QAJobsPage


@pytest.mark.parametrize("platform", ["desktop_chrome", "desktop_firefox"], indirect=True)
@allure.title("Verify QA Job Application Flow on Insider Careers Page")
@allure.feature('Career Page')
@allure.story('QA Jobs Filtering and Validation')
def test_insider_flow(driver, platform):
    home = HomePage(driver=driver, platform=platform)
    careers = CareersPage(driver=driver, platform=platform)
    qa_jobs = QAJobsPage(driver=driver, platform=platform)
    job_detail_page = JobDetailPage(driver=driver, platform=platform)

    with allure.step("Verify Insider Home Page is opened"):
        assert "Insider" in driver.title

    home.navigate_to_careers()

    with allure.step("Verify main elements are present on Careers page"):
        careers.verify_main_elements_present()
        time.sleep(3)

    with allure.step("Expand teams section and verify new sections"):
        careers.click_see_all_teams()
        careers.verify_team_sections_visible()

    location = "Istanbul, Turkiye"
    department = "Quality Assurance"
    time.sleep(3)
    qa_jobs.open_qa_page()

    qa_jobs.click_see_all_jobs()
    time.sleep(3)
    qa_jobs.accept_cookies()
    time.sleep(3)
    qa_jobs.apply_filters(location=location, department=department)
    expected_title = "Quality Assurance"
    expected_department = "Quality Assurance"
    driver.execute_script("window.scrollBy(0,500);")
    time.sleep(3)
    with allure.step("Verify all job listings match selected filters"):
        assert qa_jobs.verify_job_listings(
            expected_title=expected_title,
            expected_department=expected_department,
            expected_location=location
        )

    expected_position_header = "Senior Software Quality Assurance Engineer"

    with allure.step("Verify that correct job detail page is opened"):
        job_detail_page.find_job_and_click_view_role(expected_position_header)
        driver.switch_to.window(driver.window_handles[-1])
        assert job_detail_page.get_position_header_text() == expected_position_header
        assert "We are Insider, a B2B SaaS company that drives growth for its clients around the world. How are we achieving this? We are the #1 AI-native platform for Customer Experience and Marketing—offers marketers" in job_detail_page.get_job_description_text()
