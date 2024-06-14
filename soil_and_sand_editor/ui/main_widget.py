from __future__ import annotations

from typing import TYPE_CHECKING

from soil_and_sand_editor.scene.update_scene import renew_scene

if TYPE_CHECKING:
    from soil_and_sand_editor.ui.main_ui import SoilAndDustEditorMainUI
import glob
import pathlib
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtCore import QDir, Qt, QFileInfo, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QWidget, QGridLayout, QFileSystemModel, QTreeView, QScrollArea, QLabel, QBoxLayout, \
    QSplitter, QListWidget, QTabWidget

from soil_and_sand_editor.pixmap.pixmap import pixmaps_static
from soil_and_sand_editor.map.map_io import read_file
from soil_and_sand_editor.ui.extend.edit_map_scene import ExtendMapScene
from soil_and_sand_editor.ui.extend.extend_graphic_view import ExtendGraphicView
from soil_and_sand_editor.ui.extend.extend_list_widget import ExtendListWidgetItem
from soil_and_sand_editor.ui.extend.qthread_worker import QThreadWorker
from soil_and_sand_editor.utils.multi_language.language_wrapper import language_wrapper


def load_and_update_pixmap(tile_list_widget: QListWidget, load_path: str, pixmap_type: str, tile_size: int):
    pngs = glob.glob(load_path)
    for png in pngs:
        pixmap = QPixmap(png)
        list_pixmap = pixmap.scaled(tile_size, tile_size, Qt.AspectRatioMode.KeepAspectRatio)
        png_path = Path(png)
        png_name = png_path.name
        list_item = ExtendListWidgetItem(list_pixmap, "")
        list_item.png_name = png_name
        tile_list_widget.addItem(list_item)
        if pixmap_type == "floor":
            height = tile_size
            width = tile_size
        else:
            height = pixmap.height()
            width = pixmap.width()
        pixmaps_static.update({png_name: {
            "pixmap": pixmap, "pixmap_type": pixmap_type,
            "height": height, "width": width,
        }})


class MainWidget(QWidget):

    def __init__(self, main_ui: SoilAndDustEditorMainUI, tile_size: int = 60, grid_max_size_x: int = 12000,
                 grid_max_size_y: int = 12000):
        super().__init__()
        # Init var
        self.main_ui = main_ui
        self.tile_size = tile_size
        self.grid_max_size_x = grid_max_size_x
        self.grid_max_size_y = grid_max_size_y
        # Layout init
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        # Treeview
        self.project_treeview_model = QFileSystemModel()
        self.project_treeview_model.setRootPath(QDir.currentPath())
        self.project_treeview_model.setNameFilters(["*.jsad"])
        self.project_treeview_model.setFilter(QtCore.QDir.Filter.Files)
        self.project_treeview_model.setNameFilterDisables(False)
        self.project_treeview = QTreeView()
        self.project_treeview.setModel(self.project_treeview_model)
        self.project_treeview.setRootIndex(
            self.project_treeview_model.index(str(Path.cwd()))
        )
        self.tree_view_scroll_area = QScrollArea()
        self.tree_view_scroll_area.setWidgetResizable(True)
        self.tree_view_scroll_area.setViewportMargins(0, 0, 0, 0)
        self.tree_view_scroll_area.setWidget(self.project_treeview)
        self.tree_view_scroll_area.setWidgetResizable(True)
        self.project_treeview.clicked.connect(self.treeview_click)
        # TabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        # choose block area
        self.tile_name_label = QLabel()
        self.block_pixmap_label = QLabel()
        self.soil_floor_1_pixmap = QPixmap("assets/tiles/soil_floor_1.png")
        self.soil_floor_1_pixmap = self.soil_floor_1_pixmap.scaled(
            self.tile_size, self.tile_size, Qt.AspectRatioMode.KeepAspectRatio)
        self.tile_name_label.setText("soil_floor_1")
        self.block_pixmap_label.setPixmap(self.soil_floor_1_pixmap)
        self.block_widget = QWidget()
        self.tile_widget_boxlayout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.tile_widget_boxlayout.addWidget(self.tile_name_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.tile_widget_boxlayout.addWidget(self.block_pixmap_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.block_widget.setLayout(self.tile_widget_boxlayout)
        # List widget
        # Tile
        self.tile_list_widget = QListWidget()
        self.tile_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.tile_list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.tile_list_widget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tile_list_widget.itemClicked.connect(self.list_widget_click)
        self.plant_list_widget = QListWidget()
        self.plant_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.plant_list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.plant_list_widget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plant_list_widget.itemClicked.connect(self.list_widget_click)
        self.furniture_list_widget = QListWidget()
        self.furniture_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.furniture_list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.furniture_list_widget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.furniture_list_widget.itemClicked.connect(self.list_widget_click)
        self.collision_list_widget = QListWidget()
        self.collision_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.collision_list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.collision_list_widget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.collision_list_widget.itemClicked.connect(self.list_widget_click)
        self.tab_widget.addTab(
            self.tile_list_widget, language_wrapper.language_word_dict.get("tab_name_tile"))
        self.tab_widget.addTab(
            self.plant_list_widget, language_wrapper.language_word_dict.get("tab_name_plant"))
        self.tab_widget.addTab(
            self.furniture_list_widget, language_wrapper.language_word_dict.get("tab_name_building"))
        self.tab_widget.addTab(
            self.collision_list_widget, language_wrapper.language_word_dict.get("tab_name_collision"))
        self.tile_splitter = QSplitter()
        self.tile_splitter.setOrientation(Qt.Orientation.Vertical)
        self.tile_splitter.addWidget(self.block_widget)
        self.tile_splitter.addWidget(self.tab_widget)
        self.tile_splitter.setSizes([100, 500])
        # Load basic tiles
        load_and_update_pixmap(
            self.tile_list_widget, "assets/tiles/*.png", "floor", tile_size)
        load_and_update_pixmap(
            self.plant_list_widget, "assets/plant/*.png", "plant", tile_size)
        load_and_update_pixmap(
            self.furniture_list_widget, "assets/object/*.png", "object", tile_size)
        load_and_update_pixmap(
            self.collision_list_widget, "assets/collision/*.png", "collision", tile_size)
        # Graphics view
        self.opengl_widget = QOpenGLWidget()
        self.graphics_view = ExtendGraphicView(self.opengl_widget)
        self.edit_map_scene = ExtendMapScene(
            block_size=self.tile_size,
            grid_max_size_x=self.grid_max_size_x, grid_max_size_y=self.grid_max_size_y,
            default_pixmap=self.soil_floor_1_pixmap, default_name="soil_floor_1.png")
        self.graphics_view.setScene(self.edit_map_scene)
        # Add to ui
        self.full_splitter = QSplitter(self)
        self.full_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.full_splitter.addWidget(self.tree_view_scroll_area)
        self.full_splitter.addWidget(self.graphics_view)
        self.full_splitter.addWidget(self.tile_splitter)
        self.full_splitter.setSizes([100, 500, 100])
        self.grid_layout.addWidget(self.full_splitter, 0, 0)
        self.setLayout(self.grid_layout)

    def treeview_click(self) -> None:
        clicked_item: QFileSystemModel = self.project_treeview.selectedIndexes()[0]
        file_info: QFileInfo = self.project_treeview.model().fileInfo(clicked_item)
        path = pathlib.Path(file_info.absoluteFilePath())
        if path.is_file() and path.suffix == ".jsad":
            read_thread = QThreadWorker(read_file, str(path))
            read_thread.signal.finished.connect(lambda: renew_scene(self.main_ui))
            thread_pool = self.main_ui.thread_pool
            thread_pool.start(read_thread)

    def list_widget_click(self, clicked_item: ExtendListWidgetItem) -> None:
        self.tile_name_label.setText(clicked_item.png_name)
        pixmap_setting = pixmaps_static.get(clicked_item.png_name)
        pixmap = pixmap_setting.get("pixmap")
        pixmap_type = pixmap_setting.get("pixmap_type")
        self.block_pixmap_label.setPixmap(pixmap)
        if pixmap_type == "floor":
            self.edit_map_scene.current_pixmap = clicked_item.icon().pixmap(
                QSize(self.tile_size, self.tile_size))
        else:
            self.edit_map_scene.current_pixmap = pixmap
        self.edit_map_scene.current_pixmap_name = clicked_item.png_name

    def close(self):
        super().close()
