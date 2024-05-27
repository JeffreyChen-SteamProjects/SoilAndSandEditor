from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QAction

from soil_and_dust_editor.map.map_io import save_structure_file, read_structure_file
from soil_and_dust_editor.scene.update_scene import create_new_map_scene
from soil_and_dust_editor.ui.dialog.new_file_dialog import NewFileDialog
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
    main_ui.file_menu.read_file_action.triggered.connect(lambda: read_structure_file(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.read_file_action)


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
