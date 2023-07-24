from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class OutputLogsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the tab
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add a label and a text field to the tab
        self.label = QLabel("Output Logs:")
        self.layout.addWidget(self.label)
        self.text_field = QTextEdit()
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field)
