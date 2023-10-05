from . import *
from PyQt6.QtCore import Qt, QItemSelectionModel
from PyQt6.QtGui import QFont, QTransform, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QStyle
from Cyber_Scripts import *
from Main.cyber_attacks_container import CyberContainer
from .CyberScriptsTab import CyberScriptsTab


class AIOTab(QWidget):
    def __init__(self):
        super().__init__()

        # create layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # create UI box
        self.ui = TabUI()  # self.cyber_container)
        # create button
        self.begin_button = QPushButton("Begin")
        self.begin_button.clicked.connect(self.begin)

        # add QWidgets
        self.layout.addWidget(self.ui, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.begin_button, alignment=Qt.AlignmentFlag.AlignRight)

    def begin(self):
        self.ui.begin()


class TabUI(QWidget):
    def __init__(self):
        super().__init__()
        # attributes
        self.script_names = list_package_modules("Cyber_Scripts")

        # target lists
        self.existing_targets = {}
        self.active_targets = {}

        # target forms

        # create layout
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # create and add "scripts"
        self.scripts = QListWidget(parent=self)
        self.load_scripts()
        self.layout.addWidget(self.scripts)

        # create and add "existing target objects"
        self.existing_targets_widget = self.existing_targets[self.script_names[0]]
        self.layout.addWidget(self.existing_targets_widget)

        # connect event functions
        self.scripts.itemClicked.connect(self.script_selected)

        # create and add "new target objects"
        self.new_targets = None  # once a script is selected create instance of NewTarget()

    def load_scripts(self):
        self.scripts.addItems(self.script_names)
        for script in self.script_names:
            self.existing_targets[script] = QListWidget(parent=self)
            self.existing_targets[script].setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            self.active_targets[script] = []

    def script_selected(self):
        self.load_existing_targets()
        self.load_form()

    def load_existing_targets(self):
        script = self.scripts.selectedItems()[0].text()
        self.existing_targets_widget = self.existing_targets[script]

    def load_form(self):
        pass

    def save_data(self):
        """save all the data in the ui"""
        pass

    def load_data(self):
        """load saved data to the ui"""
        pass

    def load_ui(self):
        pass

    def select_all(self):
        pass

    def deselect_all(self):
        pass

    def begin(self):
        pass


class DataObject(QWidget):
    def __init__(self, script, data_dict):
        super().__init__()

        self.script = script
        self.data = data_dict
        self.success = None
        self.time = -1

    def get_address(self):
        return self.data["address"]


class TargetListItem(QWidget):
    def __init__(self, script: str, data: DataObject, parent_item: QListWidgetItem, parent_list: QListWidget):
        super().__init__()
        # attributes
        self.parent_item = parent_item
        self.parent_list = parent_list
        self.data = data
        self.script = script

        # layout
        layout = QHBoxLayout()

        # elements
        active_checkbox = QCheckBox()
        label = QLabel(self.data.get_address())
        delete_button = QPushButton("X")

        delete_button.clicked.connect(self.delete_item)

        layout.addWidget(active_checkbox)
        layout.addWidget(label)
        layout.addWidget(delete_button)
        self.setLayout(layout)

    def delete_item(self):
        self.parent_list.takeItem(self.parent_list.row(self.parent_item))
        self.deleteLater()


class NewTarget(QWidget):
    def __init__(self, script):
        super().__init__()

        self.label_dict = {
            "SQL": ["address", "user_name"],
            "DOS": ["address"],
            "RCE": ["address", "view"]
        }
        self.field_dict = {}
        self.create_fields(script)

    def create_fields(self, script):
        for label in self.label_dict[script]:
            self.create_row(label)

    def create_row(self, label):
        pass
