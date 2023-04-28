from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit


class IPAddressTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the tab
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add a label and a text field to the tab
        self.label = QLabel("IP Address:")
        self.layout.addWidget(self.label)
        self.text_field = QLineEdit()
        self.layout.addWidget(self.text_field)

        # Add a circular button to the tab
        self.button = QPushButton("+")
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("border-radius: 25px; background-color: #f2f2f2;")
        self.layout.addWidget(self.button)
