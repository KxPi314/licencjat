import random
from map_elements import Map, Tile
from textures_and_data import TileTypes


class Algorithm:
    _map: Map
    tile_types: TileTypes

    def __init__(self, _map: Map, tile_type: TileTypes, grid_size: (int, int)):
        self._map = _map
        self.tile_types = tile_type
        self.grid_size = grid_size

    def generate_map_grid(self) -> [[Tile]]:
        pass


class WFC(Algorithm):
    neighbours_dict: dict
    grid: [[Tile]]

    def __init__(self, _map, tile_types, grid_size):
        super().__init__(_map, tile_types, grid_size)
        self.till_end = self.grid_size[0] * self.grid_size[1]
        self.grid = _map.grid.copy()
        # just for test
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                _type = str(random.randint(1, 5))+','+str(random.randint(1, 8))
                self.grid[i][j] = Tile(i, j, [_type], _type, True, 1.0)
                self.collapse_cell(self.grid[i][j])
        _map.grid = self.grid
        #------------------
        self.tile_types = tile_types

    def end_collapse(self) -> bool:
        return self.till_end == 0

    def collapse_cell(self, cell: Tile):
        cell.tile_type_name = self.find_best_option(cell.options)
        cell.collapsed = True
        self.till_end -= 1

    @staticmethod
    def find_best_option(options: [str]) -> str:
        return max(options, key=lambda x: x[1])

    def find_best_cell(self) -> Tile:
        return min(self.grid, key=lambda tile: len(tile.options))

    def update_near_collapsed(self, cell: Tile):
        x = cell.row
        y = cell.col
        for i in range(-1, 2):
            for j in range(-1, 2):
                # można zapisać inaczej
                if not(i == 0 and j == 0):
                    options = self.neighbours_dict[self.grid[x][y].tile_type_name][(i + 1) * 3 + (j + 1)]
                    self.grid[x + i][y + j].update(options)

    def collapse_all(self):
        x = random.randint(0, len(self.grid) - 1)
        y = random.randint(0, len(self.grid[0]) - 1)
        cell = self.grid[x][y]
        while self.end_collapse():
            self.collapse_cell(cell)
            self.update_near_collapsed(cell)
            cell = self.find_best_cell()

    def read_neighbours_dict(self, neighbours_data_path):
        with open(neighbours_data_path, 'r') as file:
            file.readline()
            self.neighbours_dict = {}
            for line in file.readlines():
                neighbours = [set() for _ in range(8)]
                line = line.removesuffix("\n").split(';')
                key = line[0]
                temp = [x.split("/") for x in line[1:]]
                for index, direction in enumerate(temp):
                    values = set()
                    for elem in direction:
                        name_value = elem.split("-")
                        values.add((name_value[0], float(name_value[1])))
                    neighbours[index] = values
                self.neighbours_dict[key] = neighbours


class Alg2(Algorithm):
    pass


class Alg3(Algorithm):
    pass
