import json
import time

import pytest
from selenium import webdriver
from utilities.utils import perform_login

@pytest.fixture(scope="session")
def driver():
    time.sleep(3)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(2560, 1800)
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--username", action="store", help="username for login")
    parser.addoption("--password", action="store", help="password for login")

@pytest.fixture(scope="session")
def credentials(pytestconfig):
    return {
        "username": pytestconfig.getoption("username"),
        "password": pytestconfig.getoption("password")
    }

@pytest.fixture(scope="session")
def login(driver, credentials):
    login_url = "http://localhost:3000/login"  #https://discover-dev.elastiq.ai/login
    driver.get(login_url)
    driver.maximize_window()
    perform_login(driver, credentials)
    time.sleep(2)
    return driver



