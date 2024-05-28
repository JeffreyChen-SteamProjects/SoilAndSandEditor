map_structure = {
    "grid_x": None,
    "grid_y": None,
    "block_size": None,
}


def build_block_structure(x_position: int, y_position: int, block_count: int, grid_size: int) -> dict:
    return {
        f"block_{block_count}": {
            "x": x_position,
            "y": y_position,
            "height": grid_size,
            "width": grid_size,
            "tiles": {},
            "pixmap_items": [],
        }
    }
