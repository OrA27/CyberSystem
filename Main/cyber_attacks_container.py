from PyQt6.QtWidgets import QTextEdit
import os
import importlib.util


# this is a container class for all the cyberattacks
# this requires us to change each scripts into functions
# this class will call the function in each file
# it has a reference to the QTextEdit element in the GUI class which will be used in all other functions
# that way we can write into the text box from other classes/functions which are found on different files and folders


class CyberContainer:
    def __init__(self, package_name):
        self.package = package_name
        self.output = QTextEdit()
        self.module_obj = None
        self.addresses = []
        self.active_scripts = []

    def get_script_module(self, script_name):
        full_name = f"{self.package}.{script_name}"
        module = importlib.import_module(full_name)
        return module

    def execute_script(self, address, script_name):
        module = self.get_script_module(script_name)
        module.execute(address, self.output)

    def begin(self):
        for address in self.addresses:
            for script in self.active_scripts:
                self.execute_script(address, script)
