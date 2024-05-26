from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMessageBox

from soil_and_dust_editor.class_and_static.map import map_structure
from soil_and_dust_editor.ui.dialog.new_file_dialog import NewFileDialog
from soil_and_dust_editor.ui.extend.edit_map_scene import ExtendMapScene
from soil_and_dust_editor.ui.extend.qthread_worker import QThreadWorker
from soil_and_dust_editor.utils.json.json_file import write_json, read_json
from soil_and_dust_editor.utils.multi_language.language_wrapper import language_wrapper

if TYPE_CHECKING:
    from soil_and_dust_editor.ui.main_ui import SoilAndDustEditorMainUI


def set_file_menu_bar(main_ui: SoilAndDustEditorMainUI):
    main_ui.file_menu = main_ui.menubar.addMenu(language_wrapper.language_word_dict.get("file_menu_label"))
    # New file
    main_ui.file_menu.new_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_new_file"))
    main_ui.file_menu.new_file_action.triggered.connect(lambda: new_file_dialog(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.new_file_action)
    # Write out
    main_ui.file_menu.save_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_save_file"))
    main_ui.file_menu.save_file_action.triggered.connect(lambda: save_structure_file(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.save_file_action)
    # Read
    main_ui.file_menu.read_file_action = QAction(language_wrapper.language_word_dict.get("file_menu_open_file"))
    main_ui.file_menu.read_file_action.triggered.connect(lambda: read_structure_file(main_ui))
    main_ui.file_menu.addAction(main_ui.file_menu.read_file_action)


def new_file_dialog(main_ui: SoilAndDustEditorMainUI):
    main_ui.new_file_dialog = NewFileDialog()
    main_ui.new_file_dialog.start_button.clicked.connect(
        lambda: create_new_map_scene(
            main_ui,
            main_ui.new_file_dialog.block_size_input.text(),
            main_ui.new_file_dialog.x_input.text(),
            main_ui.new_file_dialog.y_input.text()
        )
    )
    main_ui.new_file_dialog.show()


def create_new_map_scene(
        main_ui: SoilAndDustEditorMainUI, block_size: str,
        grid_max_size_x: str, grid_max_size_y: str, triggerd_by_new_file_dialog: bool = True,
        read_map: bool = False):
    if triggerd_by_new_file_dialog:
        main_ui.new_file_dialog.close()
        main_ui.new_file_dialog = None
    if block_size != "" and grid_max_size_x != "" and grid_max_size_y != "":
        block_size = int(block_size)
        grid_max_size_x = int(grid_max_size_x)
        grid_max_size_y = int(grid_max_size_y)
        if grid_max_size_x != grid_max_size_y:
            QMessageBox().warning(
                main_ui,
                language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
                language_wrapper.language_word_dict.get("new_file_dialog_waring_x_not_equal_y")
            )
        elif block_size > grid_max_size_x or block_size > grid_max_size_x:
            QMessageBox().warning(
                main_ui,
                language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
                language_wrapper.language_word_dict.get("new_file_dialog_waring_block_size_greater_than_xy")
            )
        else:
            main_ui.map_edit_scene.clear()
            default_name = main_ui.map_edit_scene.default_name
            default_image = main_ui.map_edit_scene.default_pixmap
            main_ui.map_edit_scene = None
            if triggerd_by_new_file_dialog:
                map_structure.clear()
            main_ui.map_edit_scene = ExtendMapScene(
                block_size=block_size,
                grid_max_size_x=grid_max_size_x,
                grid_max_size_y=grid_max_size_y,
                default_name=default_name,
                default_pixmap=default_image,
                read_map=read_map
            )
            main_ui.graphics_view.setScene(main_ui.map_edit_scene)
            main_ui.central_widget.edit_map_scene = main_ui.map_edit_scene
    else:
        QMessageBox().warning(
            main_ui,
            language_wrapper.language_word_dict.get("new_file_dialog_waring_tile"),
            language_wrapper.language_word_dict.get("new_file_dialog_waring_input_value")
        )


def save_structure_file(main_ui: SoilAndDustEditorMainUI):
    """
    :param main_ui: Pyside parent
    :return: save code edit content to file
    """
    file_path = QFileDialog().getSaveFileName(
        parent=main_ui,
        dir=os.getcwd(),
        filter="""Json file (*.json);;
        File (*.*)"""
    )[0]
    if file_path is not None and file_path != "":
        read_thread = QThreadWorker(output_file, file_path)
        thread_pool = main_ui.thread_pool
        thread_pool.start(read_thread)


def read_structure_file(main_ui: SoilAndDustEditorMainUI):
    file_path = QFileDialog().getOpenFileName(
        parent=main_ui,
        dir=os.getcwd(),
        filter="""Json file (*.json);;
        File (*.*)"""
    )[0]
    if file_path is not None and file_path != "":
        read_thread = QThreadWorker(read_file, file_path)
        read_thread.signal.finished.connect(lambda: renew_scene(main_ui))
        thread_pool = main_ui.thread_pool
        thread_pool.start(read_thread)


def output_file(file_path: str):
    save_structure = {}
    for key, value in map_structure.items():
        save_structure.update({
            "grid_x": map_structure.get("grid_x"),
            "grid_y": map_structure.get("grid_y"),
            "block_size": map_structure.get("block_size"),
        })
        if key not in ["grid_x", "grid_y", "block_size"]:
            new_value_dict = {}
            new_value_dict.update({
                "x": value.get("x"),
                "y": value.get("y"),
                "height": value.get("height"),
                "width": value.get("width"),
                "tiles": value.get("tiles"),
            })
            save_structure.update({key: new_value_dict})
    write_json(file_path, save_structure)


def read_file(file_path: str):
    read_structure = read_json(file_path)
    map_structure.clear()
    map_structure.update(
        {
            "grid_x": read_structure.get("grid_x"),
            "grid_y": read_structure.get("grid_y"),
            "block_size": read_structure.get("block_size"),
        }
    )
    for block_name, block_detail in read_structure.items():
        if block_name not in ["grid_x", "grid_y", "block_size"]:
            map_structure.update({block_name: {
                "x": block_detail.get("x"),
                "y": block_detail.get("y"),
                "height": block_detail.get("height"),
                "width": block_detail.get("width"),
                "tiles": block_detail.get("tiles"),
            }})


def renew_scene(main_ui: SoilAndDustEditorMainUI):
    create_new_map_scene(
        main_ui,
        map_structure.get("block_size"),
        map_structure.get("grid_x"),
        map_structure.get("grid_y"),
        False,
        True
    )
    main_ui.map_edit_scene.read_map_file()
