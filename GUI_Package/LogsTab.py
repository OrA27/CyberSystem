from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class LogsTab(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text_field = QTextEdit()
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field)

    def clear(self):
        self.text_field.clear()

