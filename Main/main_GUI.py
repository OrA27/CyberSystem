from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit

from GUI_Package.IPAddressesTab import IPAddressTab
from GUI_Package.CyberScriptsTab import CyberScriptsTab
from GUI_Package.OutputLogsTab import OutputLogsTab

import sys
from cyber_attacks_container import CyberContainer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.output = QTextEdit()
        self.cyber_container = CyberContainer("Cyber_Scripts", self.output)

        # Create the main window
        self.setWindowTitle("Cyber Security System")
        self.setGeometry(100, 100, 800, 600)

        # Create the tab widget
        self.tabs = QTabWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(IPAddressTab(self.cyber_container), "Addresses")
        self.tabs.addTab(CyberScriptsTab(self.cyber_container), "Cyber Scripts")
        self.tabs.addTab(OutputLogsTab(self.output), "Output Logs")
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
