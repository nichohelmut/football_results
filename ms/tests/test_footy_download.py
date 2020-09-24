import pytest
from selenium import webdriver
from ms.auto_download.secrets import username, password
from time import sleep
import allure


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    driver.implicitly_wait(10)
    yield
    driver.quit()


@allure.description("Clicks log in button")
@allure.severity(severity_level="NORMAL")
def test_login_click(test_setup):
    driver.get('https://footystats.org/')
    login_btn = driver.find_element_by_xpath('//*[@id="headerMenu"]/li[3]/a')

    login_btn.click()
    assert "login" in driver.current_url


@allure.description("Click on csv download button")
@allure.severity(severity_level="CRITICAL")
def test_csv_click(test_setup):
    driver.get('https://footystats.org/')
    login_btn = driver.find_element_by_xpath('//*[@id="headerMenu"]/li[3]/a')

    login_btn.click()

    enter_username(username)

    sleep(2)

    enter_password(password)

    sleep(3)

    login_btn = driver.find_element_by_xpath('//*[@id="register_submit"]')
    login_btn.click()

    sleep(4)

    csv_btn = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[1]/div[5]/a[2]')
    csv_btn.click()

    assert "download-stats-csv" in driver.current_url


def test_invalid_login(test_setup):
    driver.get('https://footystats.org/')
    login_btn = driver.find_element_by_xpath('//*[@id="headerMenu"]/li[3]/a')

    login_btn.click()

    enter_username('Hans')

    sleep(2)

    enter_password('123455')

    sleep(3)

    login_btn = driver.find_element_by_xpath('//*[@id="register_submit"]')
    login_btn.click()

    try:
        assert "download-stats-csv" not in driver.current_url
    finally:
        if (AssertionError):
            allure.attach(driver.get_screenshot_as_png(), name='invalid credentials',
                          attachment_type=allure.attachment_type.PNG)


@allure.step("Entering Username as {}".format(username))
def enter_username(user):
    email_in = driver.find_element_by_xpath('//*[@id="username"]')
    email_in.send_keys(user)


@allure.step("Entering Password as {}".format(password))
def enter_password(passw):
    pw_in = driver.find_element_by_xpath('//*[@id="password"]')
    pw_in.send_keys(passw)

# TODO: TEST CORRECT NAME DOWNLOADED CSV FILES
