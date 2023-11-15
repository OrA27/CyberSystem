from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


class OutputTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ddos_graphs = []
        self.ddos_amount = 0
        self.parent = self.parent()
        self.script_names = self.parent.input.ui.script_names
        self.rows, self.cols = 0, 0

        # layout
        self.layout = QGridLayout()
        self.main_layout = QVBoxLayout(self)

        # add a scroll bar
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_ddos_graphs(self, graphs):
        self.ddos_graphs = graphs

    def set_grid(self, rows, cols, ddos_amount):
        self.rows = rows
        self.cols = cols
        self.ddos_amount = ddos_amount

    def analyze(self, results):
        # results look like this -> result[script] = (success rate, average time)
        # currently passed means the attack failed
        i = 0
        for row in range(self.rows):
            self.layout.setRowMinimumHeight(row, 250)
            for col in range(self.cols):
                self.layout.setColumnMinimumWidth(col, 378)
                # start with ddos
                if i < self.ddos_amount:
                    graph = self.ddos_graphs[i]
                    i += 1
                    self.layout.addWidget(graph, row, col)
                    continue

                try:
                    name = self.script_names[i]  # name of current script results
                    i += 1
                    if name == "DDoS":
                        name = self.script_names[i]
                        i += 1

                    rate, avg_time = results[name]  # results
                except:
                    continue
                rate *= 100  # change from fraction to percentage

                # pie chart attributes
                fig, ax = plt.subplots()
                labels = ["Vulnerable", "resistant"]
                sizes = [rate, 100 - rate]
                colors = ['red', 'green']  # red for attack success
                explode = [0.1, 0]

                # create pie chart
                ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=False, startangle=45)
                # title and annotation of the plot
                ax.set_title(name)
                fig.text(0.5, 0.03, f'Average successful execution time: {avg_time:.2f}', ha='center')
                canvas = FigureCanvasQTAgg(fig)
                self.layout.addWidget(canvas, row, col)

    def clear(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
