import requests
from GUI_Package import *
from PyQt6.QtCore import Qt, QItemSelectionModel, pyqtSignal
from PyQt6.QtGui import QFont, QTransform, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QStyle, QListWidgetItem, \
    QCheckBox
from Cyber_Scripts import *
import validators
from Main.main_GUI import MainWindow


def get_script_module(script_name):
    full_name = f"Cyber_Scripts.{script_name}"
    module = importlib.import_module(full_name)
    return module


def execute_script(script_name, arg, output):
    module = get_script_module(script_name)
    return module.execute(*arg, output=output)


class AIOTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # create layout
        self.layout = QVBoxLayout(self)

        # create UI box
        self.ui = TabUI(self)  # self.cyber_container)
        # create button
        self.begin_button = QPushButton("Begin")
        self.begin_button.clicked.connect(self.begin)

        # add QWidgets
        self.layout.addWidget(self.ui, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.begin_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)

    def begin(self):
        self.begin_button.setEnabled(False)
        self.ui.begin()
        self.begin_button.setEnabled(True)


class TabUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        # attributes
        self.script_names = list_package_modules("Cyber_Scripts")
        self.active_script = self.script_names[0]
        self.raw_data = {}  # key: script ;; value: list of data objects
        self.container: MainWindow = self.parent().parent()
        self.log: QTextEdit = self.container.logs.text_field

        # create main layout
        self.layout = QHBoxLayout(self)  # main layout

        # create and add "scripts"
        self.scripts = QListWidget(parent=self)
        self.scripts.itemSelectionChanged.connect(self.script_selected)
        self.layout.addWidget(self.scripts)

        # create elements
        self.existing_targets = {}
        self.active_targets = {}
        self.forms = {}

        self.load_ui()

        # create and add "existing target objects"
        self.existing_targets_widget = self.existing_targets[self.active_script]
        self.active_form_widget = self.forms[self.active_script]
        self.scripts.setCurrentRow(0)
        self.existing_targets_widget.show()

        # connect event functions
        self.scripts.itemClicked.connect(self.script_selected)

        # create and add "new target objects"
        self.new_targets = None  # once a script is selected create instance of NewTarget()

        # self.layout.addWidget(self.target_list_widget)
        self.setLayout(self.layout)

    def load_ui(self):
        self.scripts.addItems(self.script_names)
        for script in self.script_names:
            new_list = QListWidget(parent=self)  # create the respective list widget

            new_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            new_list.hide()  # hide it

            # add global buttons
            # create "global buttons"
            select_all_btn = QPushButton("Select all")
            deselect_all_btn = QPushButton("Deselect all")

            deselect_all_btn.clicked.connect(self.deselect_all)
            select_all_btn.clicked.connect(self.select_all)
            se_itm = QListWidgetItem()
            dse_itm = QListWidgetItem()

            se_itm.setSizeHint(select_all_btn.sizeHint())
            dse_itm.setSizeHint(deselect_all_btn.sizeHint())

            new_list.addItem(se_itm)
            new_list.addItem(dse_itm)
            new_list.setItemWidget(se_itm, select_all_btn)
            new_list.setItemWidget(dse_itm, deselect_all_btn)

            new_form = NewTarget(script, new_list)  # create the respective form for the new targets
            new_form.hide()  # hide it

            self.layout.addWidget(new_list)  # add list to the target widget
            self.layout.addWidget(new_form)  # add form to the target widget
            self.active_targets[script] = []  # create the active target list

            self.existing_targets[script] = new_list
            self.forms[script] = new_form

    def script_selected(self):
        self.active_script = self.scripts.selectedItems()[0].text()
        self.change_existing_targets()
        self.load_form()

    def change_existing_targets(self):
        self.existing_targets_widget.hide()
        self.existing_targets_widget = self.existing_targets[self.active_script]
        self.existing_targets_widget.show()

    # def save_item(self): implemented in newTarget class

    def load_form(self):
        self.active_form_widget.hide()
        self.active_form_widget = self.forms[self.active_script]
        self.active_form_widget.clear_text_fields()
        self.active_form_widget.show()

    def save_data(self):
        """save all the data in the ui"""
        pass

    def load_data(self):
        """load saved data to the ui"""
        pass

    def select_all(self):
        targets: QListWidget = self.existing_targets_widget
        for index in range(2, targets.count()):
            item = targets.item(index)
            widget: TargetListItem = targets.itemWidget(item)
            widget.active_checkbox.setChecked(True)

    def deselect_all(self):
        targets: QListWidget = self.existing_targets_widget
        for index in range(2, targets.count()):
            item = targets.item(index)
            widget: TargetListItem = targets.itemWidget(item)
            widget.active_checkbox.setChecked(False)

    def begin(self):
        try:
            self.container.output.clear()
            self.container.logs.clear()
            print(self.container.findChildren(QTextEdit))
            for script in self.script_names:
                qlist: QListWidget = self.existing_targets[script]
                self.raw_data[script] = []
                if qlist.count() == 0:
                    continue
                for i in range(2, qlist.count()):
                    item = qlist.item(i)
                    widget: TargetListItem = qlist.itemWidget(item)
                    data: Data = widget.data
                    if widget.active_checkbox.isChecked():
                        if script == "Dos":
                            pass
                        start = time.time()
                        data.passed = execute_script(script, widget.data_to_tuple(), output=self.log)
                        finish = time.time()
                        data.time = finish - start

                        self.raw_data[script].append(data)
        except:
            return

        self.export_data()

    def item_added(self, item: QListWidgetItem):
        widget = self.existing_targets_widget.itemWidget(item)
        widget.checkboxStateChanged.connect(self.item_changed)
        widget.active_checkbox.setCheckState(Qt.CheckState.Checked)

    def item_changed(self, checked, label):
        active_list = self.active_targets[self.active_script]
        if checked and label not in active_list:
            active_list.append(label)
        else:
            active_list.remove(label)
        print(active_list)

    def export_data(self):
        results = {}
        for script in self.script_names:
            data_list: list = self.raw_data[script]
            if len(data_list) == 0:
                continue
            # (success rate, avg success time)
            success_rate = 0
            avg_time = 0
            for data in data_list:
                if data.passed:
                    success_rate += 1
                    avg_time += data.time
            avg_time /= success_rate
            success_rate /= len(data_list)
            results[script] = (success_rate, avg_time)
        self.container.output.analyze(results)  # enable later


class Data:
    def __init__(self, script):
        self.field_dict = {}
        self.script = script
        match script:
            case "SQL Injection":
                self.field_dict = {"address": None, "user name": None}
            case "RCE":
                self.field_dict = {"address": None, "view image": None}
            case "Data Interception":
                self.field_dict = {"address": None}
            case "Dos":
                self.field_dict = {"address": None}
            case "Rainbow Table":
                self.field_dict = {"address": None, "user name": None, "hashed password": None}
            case _:
                print("error")
        self.passed = None
        self.time = None

    def get_address(self):
        return self.field_dict["address"]


class TargetListItem(QWidget):
    checkboxStateChanged = pyqtSignal(bool, str)

    def __init__(self, script: str, data: Data, parent_item: QListWidgetItem, parent_list: QListWidget):
        super().__init__()
        # attributes
        self.parent_item = parent_item
        self.parent_list = parent_list
        self.data = data
        self.script = script

        # layout
        layout = QHBoxLayout()

        # elements
        self.active_checkbox = QCheckBox()
        self.label = QLabel(self.data.get_address())
        delete_button = QPushButton("X")
        delete_button.setFixedWidth(50)

        delete_button.clicked.connect(self.delete_item)
        self.active_checkbox.stateChanged.connect(self.checkbox_state_changed)

        layout.addWidget(self.active_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(delete_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def checkbox_state_changed(self):
        self.checkboxStateChanged.emit(self.active_checkbox.isChecked(), self.label.text())

    def delete_item(self):
        self.active_checkbox.setChecked(False)
        self.parent_list.takeItem(self.parent_list.row(self.parent_item))
        self.deleteLater()

    def data_to_tuple(self):
        return tuple(self.data.field_dict.values())


class NewTarget(QWidget):
    def __init__(self, script, parent_list: QListWidget):
        super().__init__()
        self.script = script
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.parent_list = parent_list
        self.field_dict = {}
        data = Data(script)
        self.create_fields(data.field_dict.keys())

    def create_fields(self, labels):
        for label in labels:
            self.create_row(label)
        btn = QPushButton("save")
        btn.clicked.connect(self.click)
        self.layout.addWidget(btn)

    def create_row(self, label):
        row = QWidget()
        layout = QHBoxLayout()
        row.setLayout(layout)
        label_w = QLabel(label)
        label_w.setFixedWidth(70)
        text_w = QLineEdit()
        layout.addWidget(label_w)
        layout.addWidget(text_w)
        self.field_dict[label] = text_w
        self.layout.addWidget(row)

    def clear_text_fields(self):
        for label in self.field_dict.keys():
            field: QLineEdit = self.field_dict[label]
            field.clear()
            field.setPlaceholderText("")

    def validate(self):
        valid_list = []
        for key in self.field_dict.keys():
            valid = True
            field: QLineEdit = self.field_dict[key]
            text = field.text()
            field.setPlaceholderText("")
            match key:
                case "address" | "view image":
                    # validate with requests
                    try:
                        response = requests.get(text)
                        if response.status_code != 200:
                            valid = False
                    except:
                        # validate with validators
                        print("No response from address")
                        valid = validators.ipv4(text) or validators.url(text)

                case "user name":
                    valid = text != ""

                case "hashed password":
                    valid = text != ""
            valid_list.append(valid)
            if not valid:
                field.clear()
                field.setPlaceholderText("Invalid input")

        return all(valid_list)

    def click(self):
        if not self.validate():
            print("fault")
            return
        new_data = Data(self.script)
        for label in self.field_dict.keys():
            new_data.field_dict[label] = self.field_dict[label].text()
            # print(label + " : " + self.data.field_dict[label])
        self.add_item(new_data)
        self.clear_text_fields()

    def add_item(self, data):
        item = QListWidgetItem()
        widget = TargetListItem(self.script, data, item, self.parent_list)
        item.setSizeHint(widget.sizeHint())
        self.parent_list.addItem(item)
        self.parent_list.setItemWidget(item, widget)
        self.parent_list.parent().item_added(item)
