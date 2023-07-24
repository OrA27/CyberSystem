from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Replace 'path_to_chromedriver' with the path to your ChromeDriver executable
# Download ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
driver = webdriver.Chrome()

# Replace 'https://example.com' with the URL of the website you want to automate
#driver.get('https://moodle2023.ruppin.ac.il/login/index.php')
#driver.get('https://www.facebook.com/')
#driver.get('https://www.instagram.com/')

# Wait for the page to load (you can use other wait strategies too)
time.sleep(2)

# Find and fill the fields with desired values
input_elements = driver.find_elements(By.TAG_NAME, "input")  # Replace 'input_field1_id' with the actual ID of the input field
input_elements = [element for element in input_elements if element.is_displayed()]
#for element in input_elements:
#    print(f'{element.get_property("name")}')
input_elements[0].send_keys('211819693')
input_elements[1].send_keys('wig2psr')

# input_field2 = driver.find_element(By.TAG_NAME, 'input')  # Replace 'input_field2_name' with the actual name of the input field
# input_field2.send_keys('wig2psr')

"""
# You can interact with dropdowns or other elements in a similar way
# For example:
# dropdown = driver.find_element_by_id('dropdown_id')
# dropdown.send_keys('Option 1')

# Submit the form (you can click buttons or perform other actions based on your specific use case)
submit_button = driver.find_element_by_xpath('//input[@type="submit"]')  # Replace the XPath with the actual XPath of the submit button
submit_button.click()

# Wait for a few seconds to observe the results before closing the browser
time.sleep(5)
"""
button_elements = driver.find_elements(By.TAG_NAME, "button")  # Replace 'input_field1_id' with the actual ID of the input field
button_elements = [element for element in button_elements if element.is_displayed() and
                   (element.get_attribute("type") == "submit" or element.get_attribute("disabled type") == "submit")]
#for element in buttons_elements:
#    print(f'{element.get_property("type")}')
print(len(button_elements))
# print(button_elements[0].get_attribute("id"))
button_elements[-1].click()

time.sleep(2)
print(driver.current_url)

# Close the browser window
driver.quit()
