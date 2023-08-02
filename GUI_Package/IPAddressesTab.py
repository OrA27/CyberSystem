from . import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTransform, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QStyle
from Main.cyber_attacks_container import CyberContainer


# TODO 30/04/2023 Amit: Connect 'enter' keypress to V button.
# TODO 30/04/2023 Amit: Validate input, both format and authorization.


class IPAddressTab(QWidget):
    def __init__(self, cyber_container: CyberContainer):
        super().__init__()

        # Create a layout for the tab
        # self.window = VerticalBox()
        # self.layout = self.window.layout
        self.cyber_container = cyber_container
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.label = QLabel("Your addresses:")  # ip tab label
        self.layout.addWidget(self.label)  # add ip tab lable to tabs layout

        # add existing ip addresses
        self.existing_ips = VerticalBox()
        self.layout.addWidget(self.existing_ips)

        self.new_ip_widget = QWidget()  # new ip widget to contain new ip layout
        self.new_ip_layout = QHBoxLayout(self.new_ip_widget)  # new ip layout to contain new ip text field and button
        self.new_ip_text_field = QLineEdit()  # creates new text field for new ip
        self.new_ip_text_field.setFixedWidth(200)

        # creates button to add and validate the new ip
        self.new_ip_button = QPushButton()
        self.new_ip_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.new_ip_button.setFixedSize(50, 50)
        self.new_ip_button.setStyleSheet("border-radius: 25px; background-color: transparent;")
        self.new_ip_button.clicked.connect(lambda: self.add_new_ip())

        # add new ip elements to the layout
        self.new_ip_layout.addWidget(self.new_ip_text_field)
        self.new_ip_layout.addWidget(self.new_ip_button)
        self.new_ip_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.new_ip_widget.setLayout(self.new_ip_layout)  # add the new ip layout to new ip widget
        self.new_ip_widget.hide()  # hide the new ip widget
        self.layout.addWidget(self.new_ip_widget)  # add new ip widget to ip tab layout
        self.setFont(QFont("Arial", 14))  # set tabs font
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # set tabs alignment

        # Add a circular button to the tab
        self.button = QPushButton()
        new_row_icon = QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton))
        # transform = QTransform().rotate(45)
        # rotated_pixmap = plus_icon.pixmap(64, 64).transformed(transform)
        # plus_icon = QIcon(rotated_pixmap)

        self.button.setIcon(new_row_icon)
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("border-radius: 25px; background-color: transparent;")
        self.button.clicked.connect(lambda: self.show_text_field())
        self.layout.addWidget(self.button)

    def show_text_field(self):
        self.new_ip_widget.show()

    def add_new_ip(self):
        self.validate_ip(self.new_ip_text_field.text())
        self.new_ip_widget.hide()

        # new class creation
        new_ip_to_add = HorizontalBox("IP", self.new_ip_text_field.text(), lambda: self.remove())
        self.existing_ips.add_row(new_ip_to_add)

        # TODO use find open ports function and add ip and ports to the list in common variables as a dict

        self.new_ip_text_field.clear()

    def validate_ip(self, ip):
        pass

    def remove(self):
        # TODO delete ip from wherever they are saved
        print("hello")
