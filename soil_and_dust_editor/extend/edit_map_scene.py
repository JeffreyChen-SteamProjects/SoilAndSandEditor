from typing import Union, List, Dict

from PySide6.QtCore import QRect, QPointF
from PySide6.QtGui import QPen, Qt, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from soil_and_dust_editor.class_and_static.map import map_structure


def build_block_structure(x_position: int, y_position: int, block_count: int, grid_size: int) -> dict:
    return {
        f"block_{block_count}": {
            "left": x_position,
            "top": y_position,
            "height": grid_size,
            "width": grid_size,
            "tiles": {},
            "pixmap_items": [],
        }
    }


def detect_block(block_structure: dict, click_position: QPointF) -> Union[None, str]:
    trigger_block = None
    for block_name, block_detail in block_structure.items():
        check_rect = QRect(
            block_detail.get("left"), block_detail.get("top"),
            block_detail.get("width"), block_detail.get("height"))
        if check_rect.contains(click_position.toPoint()):
            trigger_block = block_name
            break
    return trigger_block


class ExtendMapScene(QGraphicsScene):

    def __init__(self, grid_max_size_x: int = 500, grid_max_size_y: int = 500, block_size: int = 20,
                 default_pixmap: QPixmap = None, default_name: str = None):
        super().__init__()
        x_count = -1
        y_count = -1
        # grid_max_size x & y should be equal
        for x in range(0, grid_max_size_x + 1, block_size):
            self.addLine(x, 0, x, grid_max_size_x - 1, QPen(Qt.GlobalColor.white))
            x_count += 1
        for y in range(0, grid_max_size_y + 1, block_size):
            if y <= grid_max_size_y:
                self.addLine(0, y, grid_max_size_y - 1, y, QPen(Qt.GlobalColor.white))
                y_count += 1
        block_count = 0
        block_x_position = 0
        block_y_position = 0
        for row in range(0, y_count, 1):
            for column in range(0, x_count, 1):
                map_structure.update(build_block_structure(
                    block_x_position, block_y_position, block_count, block_size))
                block_x_position += block_size
                block_count += 1
            block_y_position += block_size
            block_x_position = 0
        self.current_pixmap = default_pixmap
        self.current_pixmap_name = default_name

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            click_position = event.scenePos()
            x = click_position.x()
            y = click_position.y()
            if x < 0 or y < 0:
                pass
            else:
                trigger_block = detect_block(map_structure, click_position)
                if trigger_block:
                    block: dict = map_structure.get(trigger_block)
                    pixmap_item: QGraphicsPixmapItem = self.addPixmap(self.current_pixmap)
                    tiles = block.get("tiles")
                    layer_count = len(tiles)
                    tile = {
                        "pixmap": self.current_pixmap,
                        "pixmap_name": "",
                        "layer": layer_count,
                        "collision": False
                    }
                    tiles.update({f"tile_{layer_count}": tile})
                    block.get("pixmap_items").append(pixmap_item)
                    pixmap_item.setX(block.get("left"))
                    pixmap_item.setY(block.get("top"))
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            click_position = event.scenePos()
            x = click_position.x()
            y = click_position.y()
            if x < 0 or y < 0:
                pass
            else:
                trigger_block = detect_block(map_structure, click_position)
                if trigger_block:
                    block: dict = map_structure.get(trigger_block)
                    items: List[QGraphicsPixmapItem] = block.get("pixmap_items")
                    tiles: Dict[str, dict] = block.get("tiles")
                    if len(items) > 0:
                        self.removeItem(items[-1])
                        items.pop()
                        tiles.popitem()
                    block.update({"pixmap_items": items})
                    block.update({"tiles": tiles})
        super().mousePressEvent(event)
