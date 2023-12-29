class Tile:
    row: int
    col: int
    walkable: bool
    tile_type_name: str
    difficult_terrain: float

    # wfc data
    options: [str]
    collapsed: bool

    def __init__(self, row, col, start_options, tile_type_name=None, walkable=True, difficult_terrain=1.0):
        self.row = row
        self.col = col
        self.collapsed = False
        self.walkable = walkable
        self.options = start_options
        self.tile_type_name = tile_type_name
        self.difficult_terrain = difficult_terrain

    def update(self, options: [str]):
        self.options = list(set(self.options) and set(options))


class Map:
    grid_size: (int, int)
    grid: [[Tile]]

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = []
        for _ in range(grid_size[0]):
            temp = []
            for _ in range(grid_size[1]):
                temp.append(None)
            self.grid.append(temp)
