from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
# from Cyber_Scripts.SQL_Injection import execute


class LogsTab(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text_field = QTextEdit()
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field)
        print(self.text_field)

"""
    def ex(self):
        execute(login_page_url="http://localhost/site/login.php", user_name="a@a.a", output=self.text_field)
"""