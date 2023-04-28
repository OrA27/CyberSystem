from PyQt5.QtWidgets import *


# from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class HorizontalBox(QWidget):
    def __init__(self, box_type, label_text):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.box_type = box_type
        self.label = QLabel(label_text)

        if box_type == "IP":
            self.button = QPushButton("")  # create the button
            icon_str = 'SP_DialogCancelButton'  # get icon name
            self.button.setToolTip("Remove this address")  # set tool tip
            self.button.clicked.connect(self.remove)  # bind action to button click
            # add widgets to layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.button)
        elif box_type == "script":
            self.button = QCheckBox()  # create the button
            icon_str = 'SP_DialogApplyButton'  # get icon name
            # add widgets to layout
            self.layout.addWidget(self.button)
            self.layout.addWidget(self.label)
        else:
            raise Exception("box type invalid")

        # style the button and set icon
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("border-radius: 25px; background-color: #f2f2f2;")
        pixmapi = getattr(QStyle, icon_str)
        icon = self.style().standardIcon(pixmapi)
        self.button.setIcon(icon)

    def remove(self):
        if self.box_type == "IP":
            pass
        else:
            raise Exception("Function and ox type mismatch")


class VerticalBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def add_row(self, row: QWidget):
        self.layout.addWidget(row)
