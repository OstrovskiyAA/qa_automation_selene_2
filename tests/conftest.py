# import allure
# import pytest
from selene import browser, be, have, Config, Browser

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config

from tests.utils import attach


# Если нужен селеноид:
@pytest.fixture(scope='function')
def setup_browser(request):
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )
    browser = Browser(Config(driver=driver))
    yield browser


    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    browser.quit()

# если без селеноида:
# @pytest.fixture(scope="function")
# def open():
#     browser.open('https://demoqa.com/automation-practice-form')