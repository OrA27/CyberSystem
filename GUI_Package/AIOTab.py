from GUI_Package import *
from PyQt6.QtCore import Qt, QItemSelectionModel
from PyQt6.QtGui import QFont, QTransform, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QStyle, QListWidgetItem, \
    QCheckBox
from Cyber_Scripts import *


# from Main.cyber_attacks_container import CyberContainer


class AIOTab(QWidget):
    def __init__(self):
        super().__init__()

        # create layout
        self.layout = QVBoxLayout(self)

        # create UI box
        self.ui = TabUI()  # self.cyber_container)
        # create button
        self.begin_button = QPushButton("Begin")
        self.begin_button.clicked.connect(self.begin)

        # add QWidgets
        self.layout.addWidget(self.ui, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.begin_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)

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

        # create main layout
        self.layout = QHBoxLayout(self)  # main layout

        # create target list widget and its layout
        # self.target_list_widget = QWidget()
        # self.target_layout = QVBoxLayout(self.target_list_widget)
        # self.target_list_widget.setLayout(self.target_layout)

        # create and add "scripts"
        self.scripts = QListWidget(parent=self)
        self.scripts.itemClicked.connect(self.script_selected)
        self.layout.addWidget(self.scripts)
        self.load_scripts()

        # create and add "existing target objects"
        self.existing_targets_widget = self.existing_targets[self.script_names[0]]
        self.existing_targets_widget.show()

        # connect event functions
        self.scripts.itemClicked.connect(self.script_selected)

        # create and add "new target objects"
        self.new_targets = None  # once a script is selected create instance of NewTarget()

        # add widgets and set layout

        # self.layout.addWidget(self.target_list_widget)
        # test - remove later
        test_widget = QLabel("test test one two three")
        self.layout.addWidget(test_widget)
        # end test
        self.setLayout(self.layout)

    def load_scripts(self):
        self.scripts.addItems(self.script_names)
        for script in self.script_names:
            new_list = QListWidget(parent=self)  # create the respective list widget

            new_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            new_list.hide()  # hide it

            self.layout.addWidget(new_list)  # add it to the target widget
            self.active_targets[script] = []  # create the active target list

            # test part - remove later
            new_list.addItem(script)
            # end test

            self.existing_targets[script] = new_list

    def script_selected(self):
        self.change_existing_targets()
        self.load_form()

    def change_existing_targets(self):
        script = self.scripts.selectedItems()[0].text()
        self.existing_targets_widget.hide()
        self.existing_targets_widget = self.existing_targets[script]
        self.existing_targets_widget.show()

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


app = QApplication(sys.argv)
AIO = AIOTab()
AIO.show()
sys.exit(app.exec())
