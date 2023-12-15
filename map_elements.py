import constant
import wave_function_collapse as wfc


class Tile:
    row: int
    col: int
    walkable: bool
    tile_type: str
    difficult_terrain: float

    def __init__(self, row, col, tile_type, walkable, difficult_terrain):
        self.row = row
        self.col = col
        self.tile_type = tile_type
        self.walkable = walkable
        self.difficult_terrain = difficult_terrain


class Map:
    grid_size: (int, int)
    grid: [[Tile]]

    def __init__(self, algorithm: str):
        self.grid_size = constant.GRID_SIZE
        self.grid = []

        if algorithm == 'wfc':
            self.grid = wfc.collapse()
        elif algorithm == 'inny':
            self.grid = "cos innego"
        else:
            self.grid = "cos innego"


