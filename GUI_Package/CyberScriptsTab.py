from . import *
from PyQt5.QtWidgets import *
from Cyber_Scripts import *
from GUI_Package import *


class CyberScriptsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the tab
        self.vertical_box = VerticalBox()
        # Search for python scripts in the project
        scripts = list_package_modules("Cyber_Scripts")
        # add checkboxes with corresponding
        for script in scripts:
            h_box = HorizontalBox('script', script)
            self.vertical_box.add_row(h_box)

        # Add a button to execute the selected python script
        self.button = QPushButton("Begin")
        self.vertical_box.layout.addWidget(self.button)
