import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a main widget to contain the two containers
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a vertical layout for the left container's buttons
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # Create a horizontal layout for the right container's tab widget
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Create a tab widget for the right container
        tab_widget = QTabWidget()
        tab_widget.setTabBarHidden(True)
        right_layout.addWidget(tab_widget)

        # Add buttons to the left container's layout
        for i in range(5):
            button = QPushButton("Tab {}".format(i + 1))
            button.setFixedSize(100, 50)
            button.setProperty("index", i)
            button.clicked.connect(self.show_tab)
            left_layout.addWidget(button)

        # Set the first button as selected
        left_layout.itemAt(0).widget().setStyleSheet("border-right: none; border-color: black;")

        # Add the layouts to the main widget
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        main_widget.setLayout(main_layout)

        # Add tabs to the tab widget
        for i in range(5):
            tab = QWidget()
            tab_widget.addTab(tab, "Tab {}".format(i + 1))

    def show_tab(self):
        # Get the index of the clicked button
        button = self.sender()
        index = button.property("index")

        # Show the corresponding tab
        tab_widget = self.centralWidget().layout().itemAt(1).layout().itemAt(0).widget()
        tab_widget.setCurrentIndex(index)

        # Set the selected button's style
        left_layout = self.centralWidget().layout().itemAt(0).layout()
        for i in range(left_layout.count()):
            left_layout.itemAt(i).widget().setStyleSheet("")
        button.setStyleSheet("border-right: none; border-color: black;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
