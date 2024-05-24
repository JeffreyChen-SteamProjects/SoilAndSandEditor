from typing import TYPE_CHECKING

from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_file_menu_bar(main_ui: SoilAndDustEditorMainUI):
    main_ui.file_menu = main_ui.menuBar().addMenu(main_ui.file_menu)
    # New file
    main_ui.file_menu.new_file_action = QAction()
    main_ui.file_menu.addAction(main_ui.file_menu.new_file_action)
    # Write out
    main_ui.file_menu.save_file_action = QAction()
    main_ui.file_menu.addAction(main_ui.file_menu.save_file_action)
    # Read
    main_ui.file_menu.read_file_action = QAction()
    main_ui.file_menu.addAction(main_ui.file_menu.read_file_action)
