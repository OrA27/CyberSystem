from Cyber_Scripts import *
from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


def execute(login_page_url, user_name):
    print("test")
    # output.append("SQL Injection Check")
    # output.append("Login page url: " + login_page_url)
    # output.append("User name: " + user_name)
    # injections = [[f"{user_name}'/*", "'*/'"], [f"{user_name}'-- ", ""]]
    injections = [[f"{user_name}'-- ", ""]]
    for injection in injections:
        passed = enter_login_input(login_page_url, injection[0], injection[1])
        if passed:
            pass
            # output.append("The Site is vulnerable to the attack\n\n")
        else:
            pass
            # output.append("The Site is not vulnerable to the attack\n\n")
        return passed

# execute(login_page_url="http://localhost/site/login.php")
