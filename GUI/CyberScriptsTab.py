import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class CyberScriptsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the tab
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Search for python scripts in the project
        directory = os.path.join(os.getcwd(), "Cyber Scripts")
        scripts = [f for f in os.listdir(directory) if f.endswith(".py")]

        # Add a list of check boxes to the tab
        self.checkboxes = []
        # for script in scripts:
        #    checkbox = QCheckBox(script)
        #    self.layout.addWidget(checkbox)
        #    self.checkboxes.append(checkbox)

        # Add a button to execute the selected python script
        self.button = QPushButton("Begin")
        self.layout.addWidget(self.button)
