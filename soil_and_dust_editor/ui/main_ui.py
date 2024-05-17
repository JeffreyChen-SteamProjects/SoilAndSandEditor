import sys

from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtWidgets import QMainWindow, QApplication
from qt_material import QtStyleTools

from soil_and_dust_editor.ui.main_widget import MainWidget


class SoilAndDustEditorMainUI(QMainWindow, QtStyleTools):

    def __init__(self, debug: bool = False):
        super().__init__()
        self.setWindowTitle("SoilAndDust")
        self.central_widget = MainWidget()
        self.setCentralWidget(self.central_widget)

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
