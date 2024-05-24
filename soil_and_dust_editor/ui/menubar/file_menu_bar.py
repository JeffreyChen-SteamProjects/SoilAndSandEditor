from __future__ import annotations

import os
import threading
from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog

from soil_and_dust_editor.class_and_static.map import map_structure
from soil_and_dust_editor.utils.json.json_file import write_json
from soil_and_dust_editor.utils.multi_language.language_wrapper import language_wrapper

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_file_menu_bar(main_ui: SoilAndDustEditorMainUI):
    main_ui.file_menu = main_ui.menubar.addMenu(language_wrapper.language_word_dict.get("file_menu_label"))
    # New file
    main_ui.file_menu.new_file_action = QAction()
    main_ui.file_menu.addAction(main_ui.file_menu.new_file_action)
    # Write out
    main_ui.file_menu.save_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_save_file"))
    main_ui.file_menu.save_file_action.triggered.connect(lambda: save_structure_file(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.save_file_action)
    # Read
    main_ui.file_menu.read_file_action = QAction()
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


def output_file(file_path: str):
    save_structure = {}
    for key, value in map_structure.items():
        value.pop("pixmap_items")
        save_structure.update({key: value})
    write_json(file_path, save_structure)
