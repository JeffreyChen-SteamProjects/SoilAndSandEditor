from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QHBoxLayout, QBoxLayout, QLineEdit, QLabel, QPushButton

from soil_and_dust_editor.utils.multi_language.language_wrapper import language_wrapper


class NewFileDialog(QWidget):

    def __init__(self, *args):
        super().__init__()
        self.box_layout = QBoxLayout(QHBoxLayout.Direction.TopToBottom)
        self.box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowTitle(language_wrapper.language_word_dict.get("new_file_dialog_window_tile"))
        self.x_layout = QHBoxLayout()
        self.x_label = QLabel(language_wrapper.language_word_dict.get("new_file_dialog_x_label"))
        self.x_input = QLineEdit()
        self.x_validator = QIntValidator(0, 999999)
        self.x_input.setValidator(self.x_validator)
        self.x_layout.addWidget(self.x_label)
        self.x_layout.addWidget(self.x_input)
        self.y_layout = QHBoxLayout()
        self.y_label = QLabel(language_wrapper.language_word_dict.get("new_file_dialog_y_label"))
        self.y_input = QLineEdit()
        self.y_validator = QIntValidator(0, 999999)
        self.y_layout.addWidget(self.y_label)
        self.y_layout.addWidget(self.y_input)
        self.block_size_layout = QHBoxLayout()
        self.block_size_label = QLabel(language_wrapper.language_word_dict.get("new_file_dialog_block_size_label"))
        self.block_size_input = QLineEdit()
        self.block_size_validator = QIntValidator(0, 999999)
        self.block_size_layout.addWidget(self.block_size_label)
        self.block_size_layout.addWidget(self.block_size_input)
        self.start_button = QPushButton(language_wrapper.language_word_dict.get("new_file_dialog_button"))
        self.box_layout.addLayout(self.x_layout)
        self.box_layout.addLayout(self.y_layout)
        self.box_layout.addLayout(self.block_size_layout)
        self.box_layout.addWidget(self.start_button)
        self.setLayout(self.box_layout)

