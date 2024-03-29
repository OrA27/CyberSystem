import math
import pickle
import requests
import validators
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

from GUI_Package import *
from Main.main_GUI import MainWindow

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from Cyber_Scripts import *

from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


class Worker(QObject):
    logged = pyqtSignal(str)
    progressed = pyqtSignal(float)
    finished = pyqtSignal(str)
    grid_sized = pyqtSignal(int, int, int)
    analyzed = pyqtSignal(dict)
    ddos_done = pyqtSignal(list)

    def __init__(self, scripts: list, targets: dict, total: int):
        super().__init__()
        self.scripts = scripts
        self.targets = targets
        self.total = total
        self.ddos_active = 0
        self.ddos_results = []
        self.raw_data = {}

    def attack(self):
        count = 1
        first_print = True
        margin_str = ""
        for script in self.scripts:
            try:
                self.raw_data[script] = []
                qlist: QListWidget = self.targets[script]
                for i in range(2, qlist.count()):
                    item = qlist.item(i)
                    widget: TargetListItem = qlist.itemWidget(item)
                    data: Data = widget.data

                    if widget.active_checkbox.isChecked():
                        # print headline and save margin in the end
                        if first_print:
                            self.logged.emit(f"{script} checks:\n")
                            margin_str = "\n"
                            first_print = False

                        # log data fields
                        vals_str = ""
                        keys_list = data.field_dict.keys()
                        final_val = list(keys_list)[-1]
                        for val in keys_list:
                            vals_str += f"{val}: {data.field_dict[val]}"
                            if val != final_val:
                                vals_str += "\n"
                        self.logged.emit(vals_str)
                        data_tuple = widget.data_to_tuple()
                        if script == "DDoS":
                            result = execute_script(script, data_tuple, output=self.logged)
                            self.logged.emit("\n")
                            if type(result) == tuple:
                                self.ddos_results.append(result)
                                self.ddos_active += 1
                            else:
                                pass

                        else:

                            # beginning of attack
                            start = time.time()  # start measure time
                            data.passed = execute_script(script, data_tuple)  # perform attack
                            finish = time.time()  # end measure time
                            data.time = finish - start  # get measurement
                            # ending attack
                            if type(data.passed) != bool:
                                self.logged.emit(f"The Check stopped due to an Error\n")
                            else:
                                if data.passed:
                                    self.logged.emit("The Site is vulnerable to the attack")
                                else:
                                    self.logged.emit("The Site is not vulnerable to the attack")
                                self.logged.emit(f'attack time: {data.time:.2f}\n')

                                self.raw_data[script].append(data)

                        self.progressed.emit((count / self.total) * 100)
                        count += 1
                self.logged.emit(margin_str)
                margin_str = ""
                first_print = True
            except Exception as e:
                self.logged.emit(f"ERROR: {e}")

        try:
            self.set_grid_size()
            self.ddos_done.emit(self.ddos_results)
        except Exception as e:
            self.logged.emit(f"ERROR: {e}")

    def export_data(self):
        results = {}
        for script in self.scripts:
            if script == "DDoS":
                continue
            data_list: list = self.raw_data[script]
            if len(data_list) == 0:
                continue

            success_rate = 0
            avg_time = 0
            for data in data_list:
                if data.passed:
                    success_rate += 1
                    avg_time += data.time
            try:
                avg_time /= success_rate
            except:
                avg_time = 0
            success_rate /= len(data_list)
            results[script] = (success_rate, avg_time)

        self.analyzed.emit(results)
        self.finished.emit('done')

    def set_grid_size(self):
        graphs_amount = (len(self.scripts) - 1) + self.ddos_active  # amount of scripts - ddos + active ddos targets
        cols = 2
        rows = math.ceil(graphs_amount/cols)
        self.grid_sized.emit(rows, cols, self.ddos_active)
        return rows, cols


class AIOTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # create layout
        self.layout = QVBoxLayout(self)

        # create UI box
        self.ui = TabUI(self)

        # create button
        self.begin_button = QPushButton("Begin")
        self.begin_button.clicked.connect(self.begin)

        # add QWidgets
        self.layout.addWidget(self.ui, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.begin_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)

    def begin(self):
        self.ui.initiate_attacks()


class TabUI(QWidget):
    set_ddos_graphs = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        # attributes
        self.script_names = list_package_modules("Cyber_Scripts")
        self.active_script = self.script_names[0]
        self.aio: AIOTab = self.parent()
        self.container: MainWindow = self.parent().parent()
        self.log: QTextEdit = self.container.logs.text_field
        self.files_paths = {}
        self.data_lists = {}

        # create main layout
        self.layout = QHBoxLayout(self)  # main layout

        # create progress bar
        self.bar = QProgressBar(self)
        self.bar.setTextVisible(False)
        self.bar.setFixedWidth(786)
        self.layout.addWidget(self.bar)
        self.bar.hide()

        # create and add "scripts"
        self.scripts = QListWidget(parent=self)
        self.scripts.setObjectName("scripts_list")
        self.scripts.itemSelectionChanged.connect(self.script_selected)
        self.layout.addWidget(self.scripts)

        # create elements
        self.existing_targets = {}
        self.active_targets = {}
        self.forms = {}

        self.load_ui()

        # create and add "existing target objects" & "active_form_widget"
        self.existing_targets_widget = self.existing_targets[self.active_script]
        self.active_form_widget = self.forms[self.active_script]
        self.scripts.setCurrentRow(0)
        self.existing_targets_widget.show()

        # Get/Set save files' paths
        self.create_save_files()

        # load all existing item
        self.load_items()

    def create_save_files(self):
        for script in self.script_names:
            self.files_paths[script] = file_path(script)
            if not os.path.exists(self.files_paths[script]):
                file = open(self.files_paths[script], "wb")
                file.close()

    def load_items(self):
        for index, script in enumerate(self.script_names):
            self.scripts.setCurrentRow(index)
            self.data_lists[script] = []
            try:
                with open(self.files_paths[script], 'rb') as file:
                    try:
                        while True:
                            instance = pickle.load(file)
                            self.data_lists[script].append(instance)
                            self.forms[script].add_item(instance, saved=True)
                    except EOFError:
                        pass
            except (FileNotFoundError, IOError):
                # Handle errors or the case where the file doesn't exist
                self.log.append(self.files_paths[script] + "not found\n\n")
        self.scripts.setCurrentRow(0)

    def save_another_item(self, data):
        self.data_lists[self.active_script].append(data)
        with open(self.files_paths[self.active_script], "ab") as file:
            pickle.dump(data, file)

    def save_all_items(self, script):
        with open(self.files_paths[script], "wb") as file:
            for data in self.data_lists[script]:
                pickle.dump(data, file)

    def remove_data_from_list(self, data):
        script = self.active_script
        self.data_lists[script].remove(data)
        self.save_all_items(script)

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

    def load_form(self):
        self.active_form_widget.hide()
        self.active_form_widget = self.forms[self.active_script]
        self.active_form_widget.clear_text_fields()
        self.active_form_widget.show()

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

    def initiate_attacks(self):
        active_targets = self.count_active_targets()
        if active_targets == 0:
            return
        try:
            # create thread & worker here
            self.worker = Worker(self.script_names, self.existing_targets, active_targets)
            self.thread = QThread()

            # move worker to thread
            self.worker.moveToThread(self.thread)

            # connect all signals and functions
            self.thread.started.connect(self.attack_setup)
            self.thread.started.connect(self.worker.attack)
            self.worker.logged.connect(self.write_log)
            self.worker.progressed.connect(self.percentage_done)
            self.worker.grid_sized.connect(self.container.output.set_grid)
            self.worker.analyzed.connect(self.container.output.analyze)
            self.worker.ddos_done.connect(self.create_ddos_graphs)
            self.set_ddos_graphs.connect(self.worker.export_data)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.finished.connect(self.return_to_default)

            # start thread
            self.thread.start()
        except Exception as e:
            self.log.append(f'ERROR: {e}')
            return

    def create_ddos_graphs(self, results):
        ddos_graphs = []
        for result in results:
            iter_list = result[0]
            response_times_list = result[1]
            num_of_threads = result[2]
            num_of_samples = result[3]
            response_avgs_between_threads = result[4]

            fig = Figure()
            ax = fig.add_subplot(111)

            # Plot code here

            ax.plot(iter_list, response_times_list)

            # naming the time in sec axis
            ax.set_xlabel('Threads')

            # naming the response time in ms axis
            ax.set_ylabel('Response time')

            # giving a title to my graph
            ax.set_title('Server response time depending on threads')

            # Set the x-axis limits to start at 0 and end at 110
            ax.set_xlim(0, num_of_samples)

            # Set tick marks on the x-axis at every 10 units
            ax.set_xticks(range(0, num_of_samples + 1, response_avgs_between_threads))

            # Enable minor ticks at intervals of 1 unit
            minor_locator = MultipleLocator(1)
            ax.xaxis.set_minor_locator(minor_locator)

            # Create custom labels for the major ticks
            major_tick_locations = range(response_avgs_between_threads,
                                         (num_of_threads * response_avgs_between_threads + 1)
                                         , response_avgs_between_threads)
            major_tick_labels = [f'Th{(loc // response_avgs_between_threads) - 1}' for loc in major_tick_locations]

            # Set major tick marks on the x-axis and apply custom labels
            ax.set_xticks(major_tick_locations)
            ax.set_xticklabels(major_tick_labels)

            ax.grid(which='both', linestyle=':', linewidth=0.5)

            canvas = FigureCanvasQTAgg(fig)

            ddos_graphs.append(canvas)

        self.container.output.set_ddos_graphs(ddos_graphs)
        self.set_ddos_graphs.emit()

    def write_log(self, txt):
        self.log.append(txt)

    def percentage_done(self, percentage):
        self.bar.setValue(int(percentage))

    def count_active_targets(self):
        counter = 0
        for script in self.script_names:
            counter += len(self.active_targets[script])

        return counter

    def item_added(self, saved, item: QListWidgetItem):
        widget = self.existing_targets_widget.itemWidget(item)
        widget.checkboxStateChanged.connect(self.item_changed)
        widget.active_checkbox.setCheckState(Qt.CheckState.Checked)

        # save the data
        if not saved:
            self.save_another_item(widget.data)

    def item_changed(self, checked, label):
        active_list = self.active_targets[self.active_script]
        if checked:
            active_list.append(label)
        else:
            active_list.remove(label)

    def attack_setup(self):
        # clear logs tab
        self.container.output.clear()
        self.container.logs.clear()

        # reset progress bar
        self.bar.setValue(0)

        # hide elements
        self.aio.begin_button.hide()
        self.active_form_widget.hide()
        self.existing_targets_widget.hide()
        self.scripts.hide()

        # show progress bar
        self.bar.show()

    def return_to_default(self):
        # hide progress bar
        self.bar.hide()

        # show elements
        self.scripts.show()
        self.existing_targets_widget.show()
        self.active_form_widget.show()
        self.aio.begin_button.show()

        # show out put tab
        self.container.tabs.setCurrentIndex(2)


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
            case "DDoS":
                self.field_dict = {"address": None, "port": None}
            case "Rainbow Table":
                self.field_dict = {"address": None, "user name": None, "hashed password": None}
            case _:
                print(f"ERROR - There is no such script {script}")  # dev only error
        self.passed = None
        self.time = None

    def get_address(self):
        return self.field_dict["address"]

    def __eq__(self, other):
        if isinstance(other, Data):
            return (self.script == other.script) and (self.field_dict == other.field_dict)
        else:
            return False


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
        delete_button.setObjectName("delete_button")

        delete_button.clicked.connect(self.delete_item)
        self.active_checkbox.stateChanged.connect(self.checkbox_state_changed)

        layout.addWidget(self.active_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(delete_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.label.setFixedWidth(100)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def __eq__(self, other):
        if isinstance(other, TargetListItem):
            return (self.parent_list == other.parent_list) and (self.data == other.data)

    def checkbox_state_changed(self):
        self.checkboxStateChanged.emit(self.active_checkbox.isChecked(), self.label.text())

    def delete_item(self):
        self.active_checkbox.setChecked(False)
        self.parent_list.takeItem(self.parent_list.row(self.parent_item))
        self.deleteLater()

        # save all other items
        self.parent_list.parent().remove_data_from_list(self.data)

    def data_to_tuple(self):
        return tuple(self.data.field_dict.values())

    def is_unique(self):
        for i in range(2, self.parent_list.count()):
            item = self.parent_list.item(i)
            widget: TargetListItem = self.parent_list.itemWidget(item)
            if self == widget:
                return False
        return True

    def set_tooltip(self):
        tooltip_string = ''
        for key, value in self.data.field_dict.items():
            if key == 'passed':
                break
            tooltip_string += f'{key}: {value}\n'
        self.parent_item.setToolTip(tooltip_string[:-1])


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
        label_w.setFixedWidth(120)
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
            valid = False
            field: QLineEdit = self.field_dict[key]
            text = field.text()
            field.setPlaceholderText("")
            match key:
                case "address" | "view image":
                    try:
                        if validators.ipv4(text):
                            ip_address = text
                        else:
                            url = text.split("/")[2:][0]
                            ip_address = socket.gethostbyname(url)

                        if ip_address == "127.0.0.1":
                            valid = True
                        else:
                            host_name = socket.gethostname()

                            # Get local IP address using socket
                            local_ip = socket.gethostbyname(host_name)

                            ip_address_parts = ip_address.split(".")
                            local_ip_parts = local_ip.split(".")
                            valid = ip_address_parts[0:2] == local_ip_parts[0:2]

                    except Exception as e:
                        valid = False
                        ui: TabUI = self.parent_list.parent()  # for readability purposes
                        ui.log.append(f'ERROR: {e}')

                case "port":
                    try:
                        valid = int(text) in range(1, 65536)
                    except:
                        valid = False

                case "user name":
                    valid = text != ""

                case "hashed password":
                    valid = text != ""

            valid_list.append(valid)
            if not valid:
                field.clear()
                field.setPlaceholderText("Invalid input")

        return all(valid_list)

    def set_placeholder_text(self, txt):
        for key in self.field_dict.keys():
            field: QLineEdit = self.field_dict[key]
            field.clear()
            field.setPlaceholderText(txt)

    def click(self):
        if not self.validate():
            return
        new_data = Data(self.script)
        for label in self.field_dict.keys():
            new_data.field_dict[label] = self.field_dict[label].text()
        self.add_item(new_data)

    def add_item(self, data, saved=False):
        item = QListWidgetItem()
        widget = TargetListItem(self.script, data, item, self.parent_list)
        if not widget.is_unique():
            self.set_placeholder_text("already exists")
            return
        item.setSizeHint(widget.sizeHint())
        self.parent_list.addItem(item)
        self.parent_list.setItemWidget(item, widget)
        self.parent_list.parent().item_added(saved=saved, item=item)
        self.clear_text_fields()
        widget.set_tooltip()
