from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QGraphicsPixmapItem

from soil_and_sand_editor.map.generation import create_perlin_str
from soil_and_sand_editor.map.map import map_structure
from soil_and_sand_editor.pixmap.pixmap import set_pixmap_item_position, pixmaps_static
from soil_and_sand_editor.utils.multi_language.language_wrapper import language_wrapper

if TYPE_CHECKING:
    from soil_and_sand_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_generate_menu(main_ui: SoilAndDustEditorMainUI):
    main_ui.generate_menu = main_ui.menubar.addMenu(language_wrapper.language_word_dict.get("generate_menu_label"))
    # Generate map action
    main_ui.generate_menu.generate_map_action = QAction(
        language_wrapper.language_word_dict.get("generate_menu_generate_map"))
    main_ui.generate_menu.generate_map_action.triggered.connect(lambda: generate_map(main_ui))
    main_ui.generate_menu.addAction(main_ui.generate_menu.generate_map_action)


def generate_map(main_ui: SoilAndDustEditorMainUI):
    block_x = main_ui.map_edit_scene.grid_max_size_x / main_ui.map_edit_scene.block_size
    perlin_str = create_perlin_str(start=1, stop=5, size=int(block_x))
    count = 0
    for block_name, block_detail in map_structure.items():
        if block_name not in ["grid_x", "grid_y", "block_size"]:
            if perlin_str[count] == "#":
                name = "grass_floor_1.png"
                pixmap_setting = pixmaps_static.get(name)
                pixmap = pixmap_setting.get("pixmap")
                pixmap_type = pixmap_setting.get("pixmap_type")
            else:
                name = "soil_floor_1.png"
                pixmap_setting: dict = pixmaps_static.get(name)
                pixmap = pixmap_setting.get("pixmap")
                pixmap_type = pixmap_setting.get("pixmap_type")
            x = block_detail.get("x")
            y = block_detail.get("y")
            tiles = block_detail.get("tiles")
            layer_count = len(tiles)
            pixmap_item: QGraphicsPixmapItem = main_ui.map_edit_scene.addPixmap(pixmap)
            tile = {
                "pixmap_name": name,
                "collision": False
            }
            block_detail.get("pixmap_items").append(pixmap_item)
            set_pixmap_item_position(
                pixmap_item, pixmap_type, x, y, tile, pixmap, main_ui.map_edit_scene.block_size)
            tiles.update({f"tile_{layer_count}": tile})
            count += 1
        else:
            continue
