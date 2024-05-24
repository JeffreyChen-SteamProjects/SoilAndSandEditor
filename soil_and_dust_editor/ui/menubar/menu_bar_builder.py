from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMenuBar

from soil_and_dust_editor.ui.menubar.grid_menu import set_grid_menu

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_menu_bar(main_ui: SoilAndDustEditorMainUI):
    main_ui.menubar = QMenuBar()
    set_grid_menu(main_ui)
    main_ui.setMenuBar(main_ui.menubar)
