from typing import Union

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem

from soil_and_sand_editor.class_and_static.layer import layer_order

pixmaps_static = {

}


def set_pixmap_item_position(pixmap_item: QGraphicsPixmapItem, pixmap_type: str,
                             x: Union[int, float], y: Union[int, float], tile: dict,
                             pixmap: QPixmap, block_size: int) -> None:
    if pixmap_type == "floor":
        pixmap_item.setX(x)
        pixmap_item.setY(y)
        pixmap_item.setZValue(layer_order.get("floor"))
    elif pixmap_type == "collision":
        pixmap_item.setX(x)
        pixmap_item.setY(y)
        pixmap_item.setZValue(layer_order.get("collision"))
        tile.update({"collision": True})
    else:
        pixmap_item.setX(x)
        if pixmap.height() > block_size:
            pixmap_item.setY((y - pixmap.height()) + block_size)
        else:
            pixmap_item.setY(y)
        pixmap_item.setZValue(layer_order.get("things"))
