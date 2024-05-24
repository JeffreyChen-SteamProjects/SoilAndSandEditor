from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtGui import QAction

from soil_and_dust_editor.utils.multi_language.language_wrapper import language_wrapper

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_grid_menu(main_ui: SoilAndDustEditorMainUI):
    main_ui.grid_menu = main_ui.menubar.addMenu(language_wrapper.language_word_dict.get("grid_menu_label"))
    # Add grid
    main_ui.grid_menu.add_grid_action = QAction(language_wrapper.language_word_dict.get("grid_menu_open_grid"))
    main_ui.grid_menu.add_grid_action.triggered.connect(main_ui.map_edit_scene.draw_gird_line)
    main_ui.grid_menu.addAction(main_ui.grid_menu.add_grid_action)
    # Remove grid
    main_ui.grid_menu.remove_grid_action = QAction(language_wrapper.language_word_dict.get("grid_menu_close_grid"))
    main_ui.grid_menu.remove_grid_action.triggered.connect(main_ui.map_edit_scene.remove_all_grid_items)
    main_ui.grid_menu.addAction(main_ui.grid_menu.remove_grid_action)
