import os
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QTimer, QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication
from qt_material import QtStyleTools

from soil_and_sand_editor.ui.main_widget import MainWidget
from soil_and_sand_editor.ui.menubar.menu_bar_builder import set_menu_bar


class SoilAndDustEditorMainUI(QMainWindow, QtStyleTools):

    def __init__(self, debug: bool = False):
        super().__init__()
        # Var
        self.new_file_dialog = None
        self.thread_pool = QThreadPool()
        self.setWindowTitle("SoilAndSandEditor")
        # Set Icon
        self.icon_path = Path(os.getcwd() + "/je_driver_icon.ico")
        self.icon = QIcon(str(self.icon_path))
        if self.icon.isNull() is False:
            self.setWindowIcon(self.icon)
        self.central_widget = MainWidget(self)
        self.map_edit_scene = self.central_widget.edit_map_scene
        self.graphics_view = self.central_widget.graphics_view
        self.setCentralWidget(self.central_widget)
        set_menu_bar(self)

        if debug:
            self.debug_timer = QTimer()
            self.debug_timer.setInterval(10000)
            self.debug_timer.timeout.connect(self.debug_close)
            self.debug_timer.start()

    def close(self):
        super().close()
        QCoreApplication.exit(0)

    @classmethod
    def debug_close(cls):
        sys.exit(0)

    def startup_setting(self) -> None:
        self.apply_stylesheet(self, "dark_amber.xml")
        self.showMaximized()


def start_soil_and_dust_editor(debug: bool = False) -> None:
    main_app = QApplication(sys.argv)
    window = SoilAndDustEditorMainUI(debug=debug)
    try:
        window.startup_setting()
    except Exception as error:
        print(repr(error))
    sys.exit(main_app.exec())
