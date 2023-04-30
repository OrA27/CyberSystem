from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pkgutil


# classes
class HorizontalBox(QWidget):
    def __init__(self, box_type, label_text):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.box_type = box_type
        self.label = QLabel(label_text)

        if box_type == "IP":
            self.button = QPushButton("")  # create the button
            # get icon name
            icon_str = 'SP_DialogCancelButton'
            pixmapi = getattr(QStyle, icon_str)
            icon = self.style().standardIcon(pixmapi)
            self.button.setIcon(icon)

            self.button.setToolTip("Remove this address")  # set tool tip
            self.button.clicked.connect(self.remove)  # bind action to button click

            # style the button and set icon
            self.button.setFixedSize(50, 50)
            self.button.setStyleSheet("border-radius: 25px; background-color: #f2f2f2;")
            # add widgets to layout
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.button)

        elif box_type == "script":
            self.button = QCheckBox()  # create the button
            # add widgets to layout
            self.layout.addWidget(self.button, alignment=Qt.AlignLeft)
            self.layout.addWidget(self.label, alignment=Qt.AlignLeft)
            self.layout.setAlignment(Qt.AlignLeft)
            self.layout.setContentsMargins(0, 10, 0, 10)

        else:
            raise Exception("box type invalid")


    def remove(self):
        if self.box_type == "IP":
            parent_layout = self.parent()
            parent_layout.layout.removeWidget(self)
            #TODO delete ip from common variables
        else:
            raise Exception("Function and ox type mismatch")


class VerticalBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def add_row(self, row: QWidget):
        self.layout.addWidget(row)


# functions
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
