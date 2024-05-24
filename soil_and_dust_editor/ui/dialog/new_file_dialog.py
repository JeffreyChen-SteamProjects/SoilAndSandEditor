from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QBoxLayout, QLineEdit, QLabel, QPushButton


class NewFileDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.box_layout = QBoxLayout(QHBoxLayout.Direction.TopToBottom)
        self.box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_layout = QHBoxLayout()
        self.x_label = QLabel()
        self.x_input = QLineEdit()
        self.x_layout.addWidget(self.x_label)
        self.x_layout.addWidget(self.x_input)
        self.y_layout = QHBoxLayout()
        self.y_label = QLabel()
        self.y_input = QLineEdit()
        self.y_layout.addWidget(self.y_label)
        self.y_layout.addWidget(self.y_input)
        self.start_button = QPushButton()
        self.box_layout.addLayout(self.x_layout)
        self.box_layout.addLayout(self.y_layout)
        self.box_layout.addWidget(self.start_button)

