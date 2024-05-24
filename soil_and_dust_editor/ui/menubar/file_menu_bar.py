from __future__ import annotations

import os
import threading
from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMessageBox

from soil_and_dust_editor.class_and_static.map import map_structure
from soil_and_dust_editor.ui.dialog.new_file_dialog import NewFileDialog
from soil_and_dust_editor.ui.extend.edit_map_scene import ExtendMapScene
from soil_and_dust_editor.utils.json.json_file import write_json
from soil_and_dust_editor.utils.multi_language.language_wrapper import language_wrapper

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_file_menu_bar(main_ui: SoilAndDustEditorMainUI):
    main_ui.file_menu = main_ui.menubar.addMenu(language_wrapper.language_word_dict.get("file_menu_label"))
    # New file
    main_ui.file_menu.new_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_new_file"))
    main_ui.file_menu.new_file_action.triggered.connect(lambda: new_file_dialog(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.new_file_action)
    # Write out
    main_ui.file_menu.save_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_save_file"))
    main_ui.file_menu.save_file_action.triggered.connect(lambda: save_structure_file(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.save_file_action)
    # Read
    main_ui.file_menu.read_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_open_file"))
    main_ui.file_menu.addAction(main_ui.file_menu.read_file_action)


def save_structure_file(main_ui: SoilAndDustEditorMainUI):
    """
    :param main_ui: Pyside parent
    :return: save code edit content to file
    """
    file_path = QFileDialog().getSaveFileName(
        parent=main_ui,
        dir=os.getcwd(),
        filter="""Json file (*.json);;
        File (*.*)"""
    )[0]
    if file_path is not None and file_path != "":
        write_out_thread = threading.Thread(target=output_file, args=(file_path, ))
        write_out_thread.daemon = True
        write_out_thread.start()


def new_file_dialog(main_ui: SoilAndDustEditorMainUI):
    main_ui.new_file_dialog = NewFileDialog()
    main_ui.new_file_dialog.start_button.clicked.connect(
        lambda: create_new_map_scene(
            main_ui,
            main_ui.new_file_dialog.block_size_input.text(),
            main_ui.new_file_dialog.x_input.text(),
            main_ui.new_file_dialog.y_input.text()
        )
    )
    main_ui.new_file_dialog.show()


def create_new_map_scene(main_ui: SoilAndDustEditorMainUI,
                         block_size: str, grid_max_size_x: str, grid_max_size_y: str):
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
        else:
            main_ui.map_edit_scene.clear()
            main_ui.map_edit_scene = None
            main_ui.map_edit_scene = ExtendMapScene(
                block_size=block_size,
                grid_max_size_x=grid_max_size_x,
                grid_max_size_y=grid_max_size_y
            )
            main_ui.graphics_view.setScene(main_ui.map_edit_scene)
    else:
        QMessageBox().warning(
            main_ui,
            language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
            language_wrapper.language_word_dict.get("new_file_dialog_waring_input_value")
        )


def output_file(file_path: str):
    save_structure = {}
    for key, value in map_structure.items():
        value.pop("pixmap_items")
        save_structure.update({key: value})
    write_json(file_path, save_structure)
