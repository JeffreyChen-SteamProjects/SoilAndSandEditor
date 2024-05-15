from PySide6.QtGui import QPen, Qt
from PySide6.QtWidgets import QGraphicsScene


class ExtendMapScene(QGraphicsScene):

    def __init__(self, grid_max_size_x: int = 501, grid_max_size_y: int = 501, grid_size: int = 20):
        super().__init__()
        for x in range(0, grid_max_size_x, grid_size):
            self.addLine(x, 0, x, grid_max_size_x, QPen(Qt.GlobalColor.white))
        for y in range(0, grid_max_size_y, grid_size):
            self.addLine(0, y, grid_max_size_y, y, QPen(Qt.GlobalColor.white))
