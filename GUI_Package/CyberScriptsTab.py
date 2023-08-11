from . import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTransform, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QStyle
from Cyber_Scripts import *
from Main.cyber_attacks_container import CyberContainer

# TODO 30/04/2023 Or: Add function to 'Begin' button


class CyberScriptsTab(QWidget):
    def __init__(self, cyber_container: CyberContainer):
        super().__init__()

        # Create a layout for the tab
        self.cyber_container = cyber_container
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # create the box for the scripts
        self.script_box = QWidget()
        self.script_box_layout = QVBoxLayout(self.script_box)
        self.layout.addWidget(self.script_box, Qt.AlignmentFlag.AlignTop)

        # Search for python scripts in the project
        scripts = list_package_modules("Cyber_Scripts")
        # create horizontal box with checkboxes and corresponding names
        for script in scripts:
            self.new_button_row(script)  # add a new checkbox button for each script

        # Add a button to execute the selected python script
        self.button = QPushButton("Begin")
        self.layout.addWidget(self.button, Qt.AlignmentFlag.AlignRight)

    def new_button_row(self, btn_text):
        # create the container and its layout
        button_row = QWidget()
        button_row.setStyleSheet("border: 2px solid red;")
        row_layout = QHBoxLayout(button_row)  # create a box layout for the button

        button = QCheckBox()  # create button
        button.setText(btn_text)  # add script name to the button
        button.clicked.connect(self.click_checkbox)  # connect the click function

        row_layout.addWidget(button, Qt.AlignmentFlag.AlignTop)  # add button to the layout
        row_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        row_layout.setContentsMargins(0, 0, 0, 0)

        self.script_box_layout.addWidget(button_row, Qt.AlignmentFlag.AlignLeft)  # add row to script box

    def click_checkbox(self):
        pass
