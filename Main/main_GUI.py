from PyQt6 import QtGui
from PyQt6.QtWidgets import QTabWidget, QMainWindow, QApplication
from GUI_Package.AIOTab import *
from GUI_Package.OutputTab import OutputTab
from GUI_Package.LogsTab import LogsTab
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create the main window
        self.setWindowTitle("Cyber Security System")

        # set geometry
        # Set the initial size of the QMainWindow
        self.setFixedSize(880, 450)

        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Create the tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.logs = LogsTab(self)
        self.input = AIOTab(self)
        self.output = OutputTab(self)

        # Add tabs to the tab widget
        self.tabs.addTab(self.input, "Input")
        self.tabs.addTab(self.logs, "Logs")
        self.tabs.addTab(self.output, "Output")

        # create top label
        self.message_of_the_day = QLabel("Made by Or Alush & Amit Hayoun")

        # Create a vertical layout for the tab widget
        self.window_vbox = QVBoxLayout()
        self.window_vbox.addWidget(self.message_of_the_day, alignment=Qt.AlignmentFlag.AlignCenter)
        self.window_vbox.addWidget(self.tabs)

        # Set the main window layout to the horizontal layout
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.window_vbox)
        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
