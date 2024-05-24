from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenuBar

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_menu_bar(main_ui: SoilAndDustEditorMainUI):
    main_ui.menubar = QMenuBar()
    main_ui.setMenuBar(main_ui.menubar)
