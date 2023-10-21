import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QGridLayout


class OutputTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = self.parent()
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
                try:
                    name = self.script_names[i]  # name of current script results
                    rate, avg_time = results[name]  # results
                except:
                    continue
                rate *= 100  # change from fraction to percentage

                # pie chart attributes
                canvas = Canvas(self)
                labels = ["Fail", "Passed"]
                sizes = [rate, 100 - rate]
                colors = ['red', 'green']  # red for attack success
                explode = [0.1, 0]

                # create pie chart
                canvas.axes.pie(sizes, explode=explode, labels=labels, colors=colors,
                                autopct='%1.1f%%', shadow=True, startangle=90)
                # title and annotation of the plot
                canvas.axes.set_title(name)
                canvas.fig.text(0.5, 0.05, f'Average successful execution time: {avg_time}', ha='center')
                self.layout.addWidget(canvas, row, col)
                i += 1

    def clear(self):
        # Remove all widgets from the layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)
