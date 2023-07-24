from . import *
from PyQt5.QtWidgets import *
from Cyber_Scripts import *
#from GUI_Package import *


# TODO 30/04/2023 Or: Add function to 'Begin' button


class CyberScriptsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the tab
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # create the box for the scripts
        self.script_box = VerticalBox()
        self.layout.addWidget(self.script_box, alignment=Qt.AlignTop)

        # Search for python scripts in the project
        scripts = list_package_modules("Cyber_Scripts")
        # create horizontal box with checkboxes and corresponding names
        for script in scripts:
            h_box = HorizontalBox('script', script)
            self.script_box.add_row(h_box)  # add row to the script box

        # Add a button to execute the selected python script
        self.button = QPushButton("Begin")
        self.layout.addWidget(self.button, alignment=Qt.AlignRight)
