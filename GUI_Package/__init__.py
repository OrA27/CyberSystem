from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pkgutil


class HorizontalBox(QWidget):
    def __init__(self, box_type, label_text, func=None):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.box_type = box_type
        self.label = QLabel(label_text)
        self.func = func

        if box_type == "IP":
            self.button = QPushButton("")
            self.button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))

            self.button.setToolTip("Remove this address")  # set tool tip
            self.button.clicked.connect(self.remove)  # bind action to button click

            # style the button and set icon
            self.button.setFixedSize(50, 50)
            self.button.setStyleSheet("border-radius: 25px; background-color: transparent;")
            # set size of label
            self.label.setFixedWidth(190)
            self.label.setToolTip(self.label.text())
            # add widgets to layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignLeft)

        elif box_type == 'script':
            self.button = QCheckBox()  # create the button
            self.button.setText(label_text)
            # TODO add connect function to the button

            # add widgets to layout
            self.layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignLeft)
            # self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.layout.setContentsMargins(0, 10, 0, 10)

        else:
            raise Exception("box type invalid")

    def remove(self):
        if self.box_type == "IP":
            parent_layout = self.parent()
            parent_layout.layout.removeWidget(self)
            self.func()
        else:
            raise Exception("Function and box type mismatch")


class VerticalBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

    def add_row(self, row: QWidget):
        self.layout.addWidget(row)


def list_package_modules(package_name):
    """
    List all the modules of a given package, ignoring any submodules.
    """
    package = __import__(package_name)
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__):
        if not ispkg:
            modules.append(modname)
    return modules
