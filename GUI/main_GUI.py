from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

from GUI_Package.IPAddressesTab import IPAddressTab
from GUI_Package.CyberScriptsTab import CyberScriptsTab
from GUI_Package.OutputLogsTab import OutputLogsTab

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main window
        self.setWindowTitle("Cyber Security System")
        self.setGeometry(100, 100, 800, 600)

        # Create the tab widget
        self.tabs = QTabWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(IPAddressTab(), "Addresses")
        self.tabs.addTab(CyberScriptsTab(), "Cyber Scripts")
        self.tabs.addTab(OutputLogsTab(), "Output Logs")
        self.tabs.addTab(QWidget(), "Blank 1")
        self.tabs.addTab(QWidget(), "Blank 2")

        # create authors label
        self.message_of_the_day = QLabel("Testing testing one two three")

        # Create a vertical layout for the tab widget
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox.addWidget(self.message_of_the_day, alignment=Qt.AlignmentFlag.AlignCenter)
        self.tab_vbox.addWidget(self.tabs)

        # Set the main window layout to the horizontal layout
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.tab_vbox)
        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
