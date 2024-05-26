from typing import Union, List, Dict

from PySide6.QtCore import QRect, QPointF
from PySide6.QtGui import QPen, Qt, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from soil_and_dust_editor.class_and_static.map import map_structure
from soil_and_dust_editor.class_and_static.pixmap import pixmaps_static


def build_block_structure(x_position: int, y_position: int, block_count: int, grid_size: int) -> dict:
    return {
        f"block_{block_count}": {
            "x": x_position,
            "y": y_position,
            "height": grid_size,
            "width": grid_size,
            "tiles": {},
            "pixmap_items": [],
        }
    }


def detect_block(block_structure: dict, click_position: QPointF) -> Union[None, str]:
    trigger_block = None
    for block_name, block_detail in block_structure.items():
        if block_name not in ["grid_x", "grid_y", "block_size"]:
            check_rect = QRect(
                block_detail.get("x"), block_detail.get("y"),
                block_detail.get("width"), block_detail.get("height"))
            if check_rect.contains(click_position.toPoint()):
                trigger_block = block_name
                break
    return trigger_block


class ExtendMapScene(QGraphicsScene):

    def __init__(self, grid_max_size_x: int = 12000, grid_max_size_y: int = 12000, block_size: int = 60,
                 default_pixmap: QPixmap = None, default_name: str = None, read_map: bool = False):
        super().__init__()
        self.block_size = block_size
        self.grid_max_size_x = grid_max_size_x
        self.grid_max_size_y = grid_max_size_y
        self.default_pixmap = default_pixmap
        self.default_name = default_name
        self.current_pixmap = default_pixmap
        self.current_pixmap_name = default_name
        self.line_item = []
        self.read_map = read_map
        map_structure.update({
            "grid_x": grid_max_size_x,
            "grid_y": grid_max_size_y,
            "block_size": block_size,
        })
        self.draw_gird_line()

    def update_map_structure(self, x_count: int, y_count: int):
        block_count = 0
        block_x_position = 0
        block_y_position = 0
        for row in range(0, y_count, 1):
            for column in range(0, x_count, 1):
                map_structure.update(build_block_structure(
                    block_x_position, block_y_position, block_count, self.block_size))
                block_x_position += self.block_size
                block_count += 1
            block_y_position += self.block_size
            block_x_position = 0

    def draw_gird_line(self):
        if len(self.line_item) == 0:
            x_count = -1
            y_count = -1
            # grid_max_size x & y should be equal
            for x in range(0, self.grid_max_size_x + 1, self.block_size):
                line_item = self.addLine(x, 0, x, self.grid_max_size_x - 1, QPen(Qt.GlobalColor.white))
                self.line_item.append(line_item)
                x_count += 1
            for y in range(0, self.grid_max_size_y + 1, self.block_size):
                if y <= self.grid_max_size_y:
                    line_item = self.addLine(0, y, self.grid_max_size_y - 1, y, QPen(Qt.GlobalColor.white))
                    self.line_item.append(line_item)
                    y_count += 1
            if not self.read_map:
                self.update_map_structure(x_count, y_count)

    def remove_all_grid_items(self):
        for line in self.line_item:
            self.removeItem(line)
        self.line_item.clear()

    def read_map_file(self):
        for block_name, block_detail in map_structure.items():
            if block_name not in ["grid_x", "grid_y", "block_size"]:
                x = block_detail.get("x")
                y = block_detail.get("y")
                tiles: dict = block_detail.get("tiles")
                block_detail.update({"pixmap_items": []})
                for tile_name, tile_detail in tiles.items():
                    pixmap_setting = pixmaps_static.get(tile_detail.get("pixmap_name"))
                    pixmap_type = pixmap_setting.get("pixmap_type")
                    pixmap: QPixmap = pixmap_setting.get("pixmap")
                    pixmap_item = self.addPixmap(pixmap)
                    if pixmap_type == "floor":
                        pixmap_item.setX(x)
                        pixmap_item.setY(y)
                    elif pixmap_type == "collision":
                        pixmap_item.setX(x)
                        pixmap_item.setY(y)
                        tile_detail.update({"collision": True})
                    else:
                        pixmap_item.setX(x)
                        if pixmap.height() > self.block_size:
                            pixmap_item.setY((y - pixmap.height()) + self.block_size)
                        else:
                            pixmap_item.setY(y)
                    block_detail.get("pixmap_items").append(pixmap_item)

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
                        "pixmap_name": self.current_pixmap_name,
                        "layer": layer_count,
                        "collision": False
                    }
                    block.get("pixmap_items").append(pixmap_item)
                    pixmap_setting = pixmaps_static.get(self.current_pixmap_name)
                    pixmap_type = pixmap_setting.get("pixmap_type")
                    pixmap: QPixmap = pixmap_setting.get("pixmap")
                    if pixmap_type == "floor":
                        pixmap_item.setX(block.get("x"))
                        pixmap_item.setY(block.get("y"))
                    elif pixmap_type == "collision":
                        pixmap_item.setX(block.get("x"))
                        pixmap_item.setY(block.get("y"))
                        tile.update({"collision": True})
                    else:
                        pixmap_item.setX(block.get("x"))
                        if pixmap.height() > self.block_size:
                            pixmap_item.setY((block.get("y") - pixmap.height()) + self.block_size)
                        else:
                            pixmap_item.setY(block.get("y"))
                    tiles.update({f"tile_{layer_count}": tile})
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
