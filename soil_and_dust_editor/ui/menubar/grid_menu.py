from typing import TYPE_CHECKING

from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_grid_menu(main_ui: SoilAndDustEditorMainUI):
    main_ui.grid_menu = main_ui.menuBar().addMenu(main_ui.grid_menu)
    # Add grid
    main_ui.grid_menu.add_grid_action = QAction()
    main_ui.grid_menu.addAction(main_ui.grid_menu.add_grid_action)
    # Remove grid
    main_ui.grid_menu.remove_grid_action = QAction()
    main_ui.grid_menu.addAction(main_ui.grid_menu.remove_grid_action)
