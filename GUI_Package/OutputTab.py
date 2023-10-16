import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QGridLayout


class OutputTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        # create layout
        self.layout = QGridLayout()
