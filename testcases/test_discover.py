# import allure
import pytest
import time
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from utilities.utils import load_test_data, wait_for_element, click_element, get_element_text, retry_on_failure
from locator.locators import Page_Locators
# import functools

logging.basicConfig(level=logging.INFO)

def test_title(login):
    driver = login
    expected_title = "Elastiq Discover"
    assert driver.title == expected_title, f"Expected title to be '{expected_title}' but got '{driver.title}'"

def generate_test_id(data):
    return f"input_question={data['input_question']} and Type={data['type']}"


# @allure.story('Verify Questions for Discover')
# @allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("data", load_test_data(), ids=generate_test_id)
@retry_on_failure(retries=2, wait_time=7)
def test_discover(driver, data):
    input_questions = data['input_question']
    question_type = data['type']
    expected_answer = data.get('expected_answer')  # Get expected_answer if it exists

    time.sleep(3)
    click_element(driver, Page_Locators.NEW_SESSION_BUTTON)
    time.sleep(4)
    text_box = wait_for_element(driver, Page_Locators.TEXT_BOX)
    logging.info(f"Incoming question (Type: {question_type}): {input_questions}")
    text_box.send_keys(input_questions)
    time.sleep(5)
    text_box.send_keys(Keys.ENTER)
    time.sleep(10)
    try:
        if question_type == 'structured':
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='nav nav-tabs']")))
            time.sleep(3)
            wait_for_element(driver, Page_Locators.CHART_BUTTON)
            time.sleep(3)
            click_element(driver, Page_Locators.SOURCE_BUTTON)
            time.sleep(1)
            current_answer = get_element_text(driver, Page_Locators.SQL_DISCOVER_ANSWER)
            print(f"Answer: '{current_answer}'")
            logging.critical(f"Answer: {current_answer}")
            answer = current_answer.replace('\n', ' ')
            assert expected_answer in answer, f"Expected '{expected_answer}' but got '{current_answer}'"
        else:
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='nav nav-tabs']")))
            current_answer = get_element_text(driver, Page_Locators.DISCOVER_ANSWER)
            print(f"Answer: '{current_answer}'")
            logging.critical(f"Answer: {current_answer}")
            time.sleep(3)
            assert current_answer.lower() != "i don't know.", f"Expected a non-'I don't know' answer for question, but received '{current_answer}'"
            assert len(current_answer) > 15, f"Answer for '{input_questions}' is less than 15 characters"

            if input_questions != "Hi":
                WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='nav nav-tabs']")))
                click_element(driver, Page_Locators.SOURCE_BUTTON)
                time.sleep(4)
                click_element(driver, Page_Locators.DOCUMENTS_BUTTON)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(4)
                assert ".pdf" in driver.current_url, "The URL does not contain a PDF file"
                # time.sleep(3)
                # pdf_content = wait_for_element(driver, Page_Locators.PDF_CONTENT)
                # assert pdf_content is not None, "PDF did not open successfully"
                time.sleep(4)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)

    except Exception as e:
        logging.error(f"Error occurred for question: '{input_questions}': {str(e)}")
        raise e
