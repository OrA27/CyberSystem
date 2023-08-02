from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
import datetime


# TODO: create new log files each run,
#  naming convention will be according to current time


class OutputLogsTab(QWidget):
    def __init__(self, output_element):
        super().__init__()
        # current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") # get time stamp of current

        # Create a layout for the tab
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add a label and a text field to the tab
        self.label = QLabel("Output Logs:")
        self.layout.addWidget(self.label)
        self.text_field = output_element
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field)
