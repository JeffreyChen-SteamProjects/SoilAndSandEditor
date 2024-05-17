import glob
import pathlib
from pathlib import Path

from PySide6.QtCore import QDir, Qt, QFileInfo, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QGridLayout, QFileSystemModel, QTreeView, QScrollArea, QLabel, QBoxLayout, \
    QSplitter, QListWidget, QListWidgetItem

from soil_and_dust_editor.extend.edit_map_scene import ExtendMapScene
from soil_and_dust_editor.extend.extend_graphic_view import ExtendGraphicView
from soil_and_dust_editor.extend.extend_list_widget import ExtendListWidgetItem
from soil_and_dust_editor.static.pixmap_static import pixmaps_static


def load_floor_pixmaps(tile_list_widget: QListWidget):
    floor_pngs = glob.glob("assets/**/*.png")
    for png in floor_pngs:
        pixmap = QPixmap(png)
        pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        png_path = Path(png)
        png_name = png_path.stem
        list_item = ExtendListWidgetItem(pixmap, "")
        list_item.png_name = png_name
        tile_list_widget.addItem(list_item)
        pixmaps_static.update({png_name: pixmap})


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
        # Tile area
        self.tile_name_label = QLabel()
        self.tile_pixmap_label = QLabel()
        self.soil_floor_1_pixmap = QPixmap("assets/tiles/soil_floor_1.png")
        self.soil_floor_1_pixmap = self.soil_floor_1_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        self.tile_name_label.setText("soil_floor_1")
        self.tile_pixmap_label.setPixmap(self.soil_floor_1_pixmap)
        self.tile_widget = QWidget()
        self.tile_widget_boxlayout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.tile_widget_boxlayout.addWidget(self.tile_name_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.tile_widget_boxlayout.addWidget(self.tile_pixmap_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.tile_widget.setLayout(self.tile_widget_boxlayout)
        self.tile_list_widget = QListWidget()
        self.tile_list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.tile_list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.tile_list_widget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tile_list_widget.itemClicked.connect(self.tile_list_widget_click)
        self.tile_splitter = QSplitter()
        self.tile_splitter.setOrientation(Qt.Orientation.Vertical)
        self.tile_splitter.addWidget(self.tile_widget)
        self.tile_splitter.addWidget(self.tile_list_widget)
        self.tile_splitter.setSizes([100, 500])
        # Load basic tiles
        load_floor_pixmaps(self.tile_list_widget)
        # Graphics view
        self.normal_size_soil_floor_1_pixmap = QPixmap("assets/tiles/soil_floor_1.png")
        self.graphics_view = ExtendGraphicView()
        self.edit_map_scene = ExtendMapScene(default_pixmap=self.normal_size_soil_floor_1_pixmap)
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
        self.tile_pixmap_label.setPixmap(pixmaps_static.get(clicked_item.png_name))
        self.edit_map_scene.current_pixmap = clicked_item.icon().pixmap(QSize(20, 20))
