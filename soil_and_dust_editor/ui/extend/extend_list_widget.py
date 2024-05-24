from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QListWidgetItem


class ExtendListWidgetItem(QListWidgetItem):

    def __init__(self, pixmap: QPixmap, text: str):
        super().__init__(pixmap, text)
        self.png_name = None
