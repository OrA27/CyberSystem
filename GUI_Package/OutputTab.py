import math
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QLabel

from Main.main_GUI import MainWindow


class OutputTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent: MainWindow = self.parent()
        self.script_names = self.parent.input.ui.script_names
        self.rows, self.cols = self.get_rows_cols()

        # layout
        self.layout = QGridLayout()
        # either add message for no output or disable the tab until begin function has finished

    def get_rows_cols(self):
        scripts_amount = len(self.script_names)
        nearest_square = round(math.sqrt(scripts_amount)) ** 2
        rows = cols = int(math.sqrt(nearest_square))
        if scripts_amount > nearest_square:
            cols += 1
        return rows, cols

    def analyze(self, results: dict):
        # results look like this -> result[script] = (success rate, average time)
        # currently passed means the attack failed
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                name = self.script_names(i)  # name of current script results
                i += 1

                rate, avg_time = results[name]  # results
                rate *= 100  # change from fraction to percentage

                # pie chart attributes
                fig, ax = plt.subplots()
                labels = ["Fail", "Passed"]
                sizes = [rate, 100 - rate]
                colors = ['red', 'green']  # red for attack success
                explode = [0.1, 0]

                # create pie chart
                ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=True, startangle=90)

                # title and annotation of the plot
                ax.set_title(name)
                ax.annotate(f'Average successful execution time: {avg_time}')
                canvas = FigureCanvas(fig)
                self.layout.addWidget(canvas, row, col)

    def clear(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
