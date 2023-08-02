from PyQt6.QtWidgets import QTextEdit
from Cyber_Scripts import *
import os
import importlib.util


# this is a container class for all the cyberattacks
# this requires us to change each scripts into functions
# this class will call the function in each file


class CyberContainer:
    def __init__(self, package_name, output_element: QTextEdit):
        self.scripts_package = package_name
        self.output = output_element

    def execute_script(self, script_name):
