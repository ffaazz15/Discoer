import time
import functools
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locator.locators import Page_Locators
import sys
import json
import logging



def perform_login(driver, credentials):
    email_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(Page_Locators.email)
    )
    email_field.send_keys(credentials["username"])

    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(Page_Locators.password)
    )
    password_field.send_keys(credentials["password"])

    login_button = WebDriverWait(driver, 25).until(
        EC.presence_of_element_located(Page_Locators.submit_button)
    )

    login_button.click()

def wait_for_element(driver, locator, timeout=50):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def click_element(driver, locator, timeout=50):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    element.click()
    time.sleep(2)  # Short sleep to ensure the action is registered

def get_element_text(driver, locator, timeout=50):
    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    time.sleep(2)  # Short sleep to ensure the element is fully loaded
    return element.text.strip()

def load_test_data():
    # Get the command line arguments
    args = sys.argv

    # Initialize default username
    username = "default"

    # Iterate through the arguments to find the username
    for arg in args:
        if arg.startswith("--username="):
            # Extract the username part
            username = arg.split("=")[1].split("@")[0]
            break

    # Construct the file path using the extracted username
    file_path = f"testdata/{username}.json"

    # Load the JSON file
    with open(file_path) as f:
        test_data = json.load(f)

    return test_data

def retry_on_failure(retries=3, wait_time=2):
    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    logging.warning(f"Attempt {attempt} failed with assertion error: {e}")
                    if attempt == retries:
                        raise
                    time.sleep(wait_time)
                except Exception as e:
                    logging.warning(f"Attempt {attempt} failed with unexpected error: {e}")
                    if attempt == retries:
                        raise
                    time.sleep(wait_time)
        return wrapper
    return retry_decorator
