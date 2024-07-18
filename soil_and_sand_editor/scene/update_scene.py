from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMessageBox

from soil_and_sand_editor.map.map import map_structure
from soil_and_sand_editor.ui.extend.edit_map_scene import ExtendMapScene
from soil_and_sand_editor.utils.multi_language.language_wrapper import language_wrapper

if TYPE_CHECKING:
    from soil_and_sand_editor.ui.main_ui import SoilAndDustEditorMainUI


def create_new_map_scene(
        main_ui: SoilAndDustEditorMainUI, block_size: str,
        grid_max_size_x: str, grid_max_size_y: str, triggerd_by_new_file_dialog: bool = True,
        read_map: bool = False):
    if triggerd_by_new_file_dialog:
        main_ui.new_file_dialog.close()
        main_ui.new_file_dialog = None
    if block_size != "" and grid_max_size_x != "" and grid_max_size_y != "":
        block_size = int(block_size)
        grid_max_size_x = int(grid_max_size_x)
        grid_max_size_y = int(grid_max_size_y)
        if grid_max_size_x != grid_max_size_y:
            QMessageBox().warning(
                main_ui,
                language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
                language_wrapper.language_word_dict.get("new_file_dialog_waring_x_not_equal_y")
            )
        elif block_size > grid_max_size_x or block_size > grid_max_size_y:
            QMessageBox().warning(
                main_ui,
                language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
                language_wrapper.language_word_dict.get("new_file_dialog_waring_block_size_greater_than_xy")
            )
        else:
            main_ui.map_edit_scene.clear()
            default_name = main_ui.map_edit_scene.default_name
            default_image = main_ui.map_edit_scene.default_pixmap
            current_pixmap = main_ui.map_edit_scene.current_pixmap
            main_ui.map_edit_scene = None
            if triggerd_by_new_file_dialog:
                map_structure.clear()
            main_ui.map_edit_scene = ExtendMapScene(
                block_size=block_size,
                grid_max_size_x=grid_max_size_x,
                grid_max_size_y=grid_max_size_y,
                default_name=default_name,
                default_pixmap=default_image,
                read_map=read_map
            )
            main_ui.graphics_view.setScene(main_ui.map_edit_scene)
            main_ui.central_widget.edit_map_scene = main_ui.map_edit_scene
            main_ui.map_edit_scene.current_pixmap = current_pixmap
    else:
        QMessageBox().warning(
            main_ui,
            language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
            language_wrapper.language_word_dict.get("new_file_dialog_waring_input_value")
        )


def renew_scene(main_ui: SoilAndDustEditorMainUI):
    create_new_map_scene(
        main_ui,
        map_structure.get("block_size"),
        map_structure.get("grid_x"),
        map_structure.get("grid_y"),
        False,
        True
    )
    main_ui.map_edit_scene.read_map_file()
