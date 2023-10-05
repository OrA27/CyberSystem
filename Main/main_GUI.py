from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

from GUI_Package.IPAddressesTab import IPAddressTab
from GUI_Package.CyberScriptsTab import CyberScriptsTab
from GUI_Package.OutputLogsTab import OutputLogsTab

import sys
from cyber_attacks_container import CyberContainer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cyber_container = CyberContainer("Cyber_Scripts")

        # Create the main window
        self.setWindowTitle("Cyber Security System")
        self.setGeometry(100, 100, 800, 600)

        # Create the tab widget
        self.tabs = QTabWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(IPAddressTab(self.cyber_container), "Addresses")
        self.tabs.addTab(CyberScriptsTab(self.cyber_container), "Cyber Scripts")
        self.tabs.addTab(QWidget(), "Required Data")
        self.tabs.addTab(OutputLogsTab(self.cyber_container.output), "Output Logs")
        self.tabs.addTab(QWidget(), "Blank 2")

        # create top label
        self.message_of_the_day = QLabel("Testing testing one two three")

        # create begin button
        self.begin_button = QPushButton("Begin")
        # self.begin_button.setFixedWidth(200)

        # Create a vertical layout for the tab widget
        self.window_vbox = QVBoxLayout()
        self.window_vbox.addWidget(self.message_of_the_day, alignment=Qt.AlignmentFlag.AlignCenter)
        self.window_vbox.addWidget(self.tabs)
        self.window_vbox.addWidget(self.begin_button)  # , alignment=Qt.AlignmentFlag.AlignRight)


        # Set the main window layout to the horizontal layout
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.window_vbox)
        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
