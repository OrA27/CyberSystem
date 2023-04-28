import sys
# GUI widgets import
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
# tab classes import
from IPAddressesTab import IPAddressTab
from CyberScriptsTab import CyberScriptsTab
from OutputLogsTab import OutputLogsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the main window
        self.setWindowTitle("Cyber Security System")
        self.setGeometry(100, 100, 800, 600)

        # Create the tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.West)

        # Add tabs to the tab widget
        self.tab1 = IPAddressTab()
        self.tab2 = CyberScriptsTab()
        self.tab3 = OutputLogsTab()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.addTab(self.tab1, "IP Address")
        self.tabs.addTab(self.tab2, "Cyber Scripts")
        self.tabs.addTab(self.tab3, "Output Logs")
        self.tabs.addTab(self.tab4, "Tab 4")
        self.tabs.addTab(self.tab5, "Tab 5")

        # Create a vertical layout for the tab widget
        self.tab_vbox = QVBoxLayout()
        self.tab_vbox.addWidget(self.tabs)

        # Create a horizontal layout for the tab widget and the vertical bar
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.tab_vbox)

        # Set the main window layout to the horizontal layout
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.hbox)
        self.setCentralWidget(self.main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
