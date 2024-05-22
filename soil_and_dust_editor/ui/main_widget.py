import glob
import pathlib
from pathlib import Path

from PySide6.QtCore import QDir, Qt, QFileInfo, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QGridLayout, QFileSystemModel, QTreeView, QScrollArea, QLabel, QBoxLayout, \
    QSplitter, QListWidget

from soil_and_dust_editor.class_and_static.pixmap import pixmaps_static
from soil_and_dust_editor.extend.edit_map_scene import ExtendMapScene
from soil_and_dust_editor.extend.extend_graphic_view import ExtendGraphicView
from soil_and_dust_editor.extend.extend_list_widget import ExtendListWidgetItem


def load_and_update_pixmap(tile_list_widget: QListWidget, load_path: str, pixmap_type: str):
    pngs = glob.glob(load_path)
    for png in pngs:
        pixmap = QPixmap(png)
        list_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        png_path = Path(png)
        png_name = png_path.name
        list_item = ExtendListWidgetItem(list_pixmap, "")
        list_item.png_name = png_name
        tile_list_widget.addItem(list_item)
        pixmaps_static.update({png_name: {
            "pixmap": pixmap, "type": pixmap_type,
            "height": pixmap.height(),
            "width": pixmap.width(),
        }})


def load_pixmaps(list_widget: QListWidget):
    load_and_update_pixmap(list_widget, "assets/tiles/*.png", "floor")
    load_and_update_pixmap(list_widget, "assets/tree/*.png", "tree")


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        # Treeview
        self.project_treeview_model = QFileSystemModel()
        self.project_treeview_model.setRootPath(QDir.currentPath())
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
        # choose block area
        self.tile_name_label = QLabel()
        self.block_pixmap_label = QLabel()
        self.soil_floor_1_pixmap = QPixmap("assets/tiles/soil_floor_1.png")
        self.soil_floor_1_pixmap = self.soil_floor_1_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        self.tile_name_label.setText("soil_floor_1")
        self.block_pixmap_label.setPixmap(self.soil_floor_1_pixmap)
        self.block_widget = QWidget()
        self.tile_widget_boxlayout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.tile_widget_boxlayout.addWidget(self.tile_name_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.tile_widget_boxlayout.addWidget(self.block_pixmap_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.block_widget.setLayout(self.tile_widget_boxlayout)
        self.tile_list_widget = QListWidget()
        self.tile_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.tile_list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.tile_list_widget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tile_list_widget.itemClicked.connect(self.tile_list_widget_click)
        self.tile_splitter = QSplitter()
        self.tile_splitter.setOrientation(Qt.Orientation.Vertical)
        self.tile_splitter.addWidget(self.block_widget)
        self.tile_splitter.addWidget(self.tile_list_widget)
        self.tile_splitter.setSizes([100, 500])
        # Load basic tiles
        load_pixmaps(self.tile_list_widget)
        # Graphics view
        self.normal_size_soil_floor_1_pixmap = QPixmap("assets/tiles/soil_floor_1.png")
        self.graphics_view = ExtendGraphicView()
        self.edit_map_scene = ExtendMapScene(
            default_pixmap=self.normal_size_soil_floor_1_pixmap, default_name="soil_floor_1")
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
        if path.is_file():
            pass

    def tile_list_widget_click(self, clicked_item: ExtendListWidgetItem) -> None:
        self.tile_name_label.setText(clicked_item.png_name)
        pixmap_setting = pixmaps_static.get(clicked_item.png_name)
        pixmap = pixmap_setting.get("pixmap")
        pixmap_type = pixmap_setting.get("pixmap_type")
        height = pixmap_setting.get("height")
        width = pixmap_setting.get("width")
        self.block_pixmap_label.setPixmap(pixmap)
        if pixmap_type == "floor":
            self.edit_map_scene.current_pixmap = clicked_item.icon().pixmap(QSize(20, 20))
        else:
            self.edit_map_scene.current_pixmap = clicked_item.icon().pixmap(QSize(width, height))
        self.edit_map_scene.current_pixmap_name = clicked_item.png_name
