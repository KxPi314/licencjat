class Tile:
    row: int
    col: int
    walkable: bool
    difficult_terrain: float

    def __init__(self, row, col, walkable, difficult_terrain=0.0):
        self.row = row
        self.col = col
        self.walkable = walkable
        self.difficult_terrain = difficult_terrain


class Map:
    grid_size: (int, int)
    grid: [[Tile]]

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = []
