from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog

from soil_and_sand_editor.map.map import map_structure
from soil_and_sand_editor.scene.update_scene import renew_scene
from soil_and_sand_editor.ui.extend.qthread_worker import QThreadWorker
from soil_and_sand_editor.utils.json.json_file import read_json, write_json

if TYPE_CHECKING:
    from soil_and_sand_editor.ui.main_ui import SoilAndDustEditorMainUI


def save_structure_file(main_ui: SoilAndDustEditorMainUI):
    """
    :param main_ui: Pyside parent
    :return: save code edit content to file
    """
    file_path = QFileDialog().getSaveFileName(
        parent=main_ui,
        dir=os.getcwd(),
        filter="Jsad file (*.jsad);;"
    )[0]
    if file_path is not None and file_path != "":
        read_thread = QThreadWorker(output_file, file_path)
        thread_pool = main_ui.thread_pool
        thread_pool.start(read_thread)


def read_structure_file(main_ui: SoilAndDustEditorMainUI):
    file_path = QFileDialog().getOpenFileName(
        parent=main_ui,
        dir=os.getcwd(),
        filter="Jasd file (*.jsad);;"
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
