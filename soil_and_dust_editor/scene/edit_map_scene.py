from PySide6.QtCore import QRect
from PySide6.QtGui import QPen, Qt, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem


def build_block_structure(x_position: int, y_position: int, block_count: int, grid_size: int) -> dict:
    return {
        f"block_{block_count}": {
            "left": x_position,
            "top": y_position,
            "height": grid_size,
            "width": grid_size,
            "pixmap": None
        }
    }


class ExtendMapScene(QGraphicsScene):

    def __init__(self, grid_max_size_x: int = 500, grid_max_size_y: int = 500, grid_size: int = 20,
                 default_pixmap: QPixmap = None):
        super().__init__()
        x_count = -1
        y_count = -1
        # grid_max_size x & y should be equal
        for x in range(0, grid_max_size_x + 1, grid_size):
            self.addLine(x, 0, x, grid_max_size_x - 1, QPen(Qt.GlobalColor.white))
            x_count += 1
        for y in range(0, grid_max_size_y + 1, grid_size):
            if y <= grid_max_size_y:
                self.addLine(0, y, grid_max_size_y - 1, y, QPen(Qt.GlobalColor.white))
                y_count += 1
        self.block_structure = {}
        block_count = 0
        block_x_position = 0
        block_y_position = 0
        for row in range(0, y_count, 1):
            for column in range(0, x_count, 1):
                self.block_structure.update(build_block_structure(
                    block_x_position, block_y_position, block_count, grid_size))
                block_x_position += grid_size
                block_count += 1
            block_y_position += grid_size
            block_x_position = 0
        print(self.block_structure)
        self.current_pixmap = default_pixmap

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            click_position = event.scenePos()
            x = click_position.x()
            y = click_position.y()
            if x < 0 or y < 0:
                pass
            else:
                trigger_block = None
                for block_name, block_detail in self.block_structure.items():
                    check_rect = QRect(
                        block_detail.get("left"), block_detail.get("top"),
                        block_detail.get("width"), block_detail.get("height"))
                    if check_rect.contains(click_position.toPoint()):
                        trigger_block = block_name
                        break
                if trigger_block:
                    block: dict = self.block_structure.get(trigger_block)
                    pixmap_item: QGraphicsPixmapItem = self.addPixmap(self.current_pixmap)
                    block.update({"pixmap": self.current_pixmap})
                    pixmap_item.setX(block.get("left"))
                    pixmap_item.setY(block.get("top"))
        super().mousePressEvent(event)
