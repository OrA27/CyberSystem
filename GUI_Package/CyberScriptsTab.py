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
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # create the box for the scripts
        self.script_box = QWidget()
        self.script_box_layout = QVBoxLayout(self.script_box)
        self.script_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.script_box.setLayout(self.script_box_layout)

        self.layout.addWidget(self.script_box)

        # Search for python scripts in the project
        scripts = list_package_modules("Cyber_Scripts")
        # create horizontal box with checkboxes and corresponding names
        for script in scripts:
            self.new_button_row(script)  # add a new checkbox button for each script

        # Add a button to execute the selected python script
        self.button = QPushButton("Begin")
        self.button.setFixedWidth(200)
        self.layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)

    def new_button_row(self, btn_text):
        new_script_widget = QWidget()
        new_script_widget.setFixedHeight(40)
        new_script_layout = QHBoxLayout(new_script_widget)
        new_script_widget.setLayout(new_script_layout)

        new_script_button = QCheckBox()  # create the button
        new_script_button.setText(btn_text)
        # TODO add connect function to the button

        # add widgets to layout
        new_script_layout.addWidget(new_script_button, alignment=Qt.AlignmentFlag.AlignLeft)
        new_script_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.script_box_layout.addWidget(new_script_widget)

    def click_checkbox(self):
        pass
