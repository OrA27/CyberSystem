from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QHBoxLayout


class IPAddressTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the tab
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Add a label and a text field to the tab
        #self.ip_labels_widget = QWidget()
        self.new_ip_widget = QWidget()
        #self.ip_labels_layout = QVBoxLayout(self.ip_labels_widget)
        self.new_ip_layout = QHBoxLayout(self.new_ip_widget)
        self.label = QLabel("Your sites addresses:")
        self.layout.addWidget(self.label)
        #self.layout.addWidget(self.ip_labels_widget)
        self.new_ip_text_field = QLineEdit()
        self.new_ip_button = QPushButton("V")
        self.new_ip_button.setFixedSize(50, 50)
        self.new_ip_button.setStyleSheet("border-radius: 25px; background-color: #f2f2f2;")
        self.new_ip_button.clicked.connect(lambda: add_new_ip())
        #self.new_ip_text_field.hide()
        self.new_ip_layout.addWidget(self.new_ip_text_field)
        self.new_ip_layout.addWidget(self.new_ip_button)
        self.new_ip_widget.setLayout(self.new_ip_layout)
        self.new_ip_widget.hide()
        self.layout.addWidget(self.new_ip_widget)
        self.setFont(QFont("Ariel", 14))
        self.layout.setAlignment(Qt.AlignTop)

        # Add a circular button to the tab
        self.button = QPushButton("+")
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("border-radius: 25px; background-color: #f2f2f2;")
        self.button.clicked.connect(lambda: show_text_field())
        self.layout.addWidget(self.button)

        def show_text_field():
            self.new_ip_widget.show()

        def add_new_ip():
            validate_ip()
            self.new_ip_widget.hide()
            # new class creat

        def validate_ip():
            pass

