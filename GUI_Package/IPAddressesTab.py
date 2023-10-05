from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTransform, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QStyle
from Main.cyber_attacks_container import CyberContainer
import ipaddress
from urllib.parse import urlparse
from Cyber_Scripts import *
from Main import *


# TODO 30/04/2023 Amit: Connect 'enter' keypress to V button.
# TODO 30/04/2023 Amit: Validate input, both format and authorization.


class IPAddressTab(QWidget):
    def __init__(self, cyber_container: CyberContainer):
        super().__init__()

        # Create a layout for the tab
        self.cyber_container = cyber_container
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.label = QLabel("Your addresses:")  # ip tab label
        self.layout.addWidget(self.label)  # add ip tab lable to tabs layout

        # add existing ip addresses
        self.existing_addresses = QWidget()
        existing_addresses_layout = QVBoxLayout(self.existing_addresses)
        existing_addresses_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.existing_addresses.setLayout(existing_addresses_layout)

        self.layout.addWidget(self.existing_addresses)

        self.new_ip_widget = QWidget()  # new ip widget to contain new ip layout
        self.new_ip_layout = QHBoxLayout(self.new_ip_widget)  # new ip layout to contain new ip text field and button
        self.new_ip_text_field = QLineEdit()  # creates new text field for new ip
        self.new_ip_text_field.setFixedWidth(200)

        # creates button to add and validate the new ip
        self.new_ip_button = QPushButton()
        self.new_ip_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.new_ip_button.setFixedSize(50, 50)
        self.new_ip_button.setStyleSheet("border-radius: 25px; background-color: transparent;")
        self.new_ip_button.clicked.connect(self.add_new_ip)

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
        self.button.setIcon(new_row_icon)
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("border-radius: 25px; background-color: transparent;")
        self.button.clicked.connect(self.show_text_field)
        self.layout.addWidget(self.button)

    def show_text_field(self):
        self.new_ip_widget.show()

    def add_new_ip(self):
        if self.extract_ports():
            self.new_ip_widget.hide()

            new_ip_widget = QWidget()
            new_ip_widget.setObjectName(self.new_ip_text_field.text())
            layout = QHBoxLayout(new_ip_widget)
            new_ip_widget.setLayout(layout)
            new_ip_label = QLabel(self.new_ip_text_field.text())

            new_ip_button = QPushButton("")
            new_ip_button.setIcon(new_ip_widget.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))

            new_ip_button.setToolTip("Remove this address")  # set tool tip
            new_ip_button.clicked.connect(self.remove)  # bind action to button click

            # style the button and set icon
            new_ip_button.setFixedSize(50, 50)
            new_ip_button.setStyleSheet("border-radius: 25px; background-color: transparent;")
            # set size of label
            new_ip_label.setFixedWidth(190)
            new_ip_label.setToolTip(new_ip_label.text())
            # add widgets to layout
            layout.addWidget(new_ip_label)
            layout.addWidget(new_ip_button, alignment=Qt.AlignmentFlag.AlignLeft)

            # self.existing_ips.add_row(new_ip_widget)
            self.existing_addresses.layout().addWidget(new_ip_widget)

            self.new_ip_text_field.clear()
        else:
            print("not validate address")

    """
    @staticmethod
    def is_valid_ip_address(input_string):
        try:
            ipaddress.ip_address(input_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_url(input_string):
        parsed_url = urlparse(input_string)
        return parsed_url.scheme != '' and parsed_url.netloc != ''

    def validate_address(self):
        address = self.new_ip_text_field.text()
        return self.is_valid_ip_address(address) or self.is_valid_url(address)
    """

    def extract_ports(self):
        new_address = self.new_ip_text_field.text()
        ports = [80, 8080]  # port_discovery(new_address)
        if not ports:
            return False
        self.cyber_container.addresses[new_address] = ports
        return True

    def remove(self):
        address_widget = self.sender().parent()
        address = address_widget.findChild(QLabel).text()
        all_addresses_widget = address_widget.parent()
        all_addresses_widget_layout = all_addresses_widget.layout()
        all_addresses_widget_layout.removeWidget(address_widget)
        self.cyber_container.addresses.pop(address)
