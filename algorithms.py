import random

import constant
from map_elements import Map, Tile
from textures_and_data import TileTypes


class Algorithm:
    _map: Map
    tile_types: TileTypes

    def __init__(self, _map: Map, tile_type: TileTypes):
        self._map = _map
        self.tile_types = tile_type

    def generate_map_grid(self) -> [[Tile]]:
        pass


class WCFTile(Tile):
    options: [str]
    collapsed: bool

    def __init__(self, row, col, start_options):
        super().__init__(row, col)
        # trzeba by jakieś ustalić
        self.options = start_options
        self.collapsed = False

    def update(self, options: [str]):
        self.options = self.options and options


class WFC(Algorithm):
    neighbours_dict: dict
    wfc_grid: [[WCFTile]]

    def __init__(self, _map, tile_types):
        super().__init__(_map, tile_types)
        self.read_neighbours_dict(constant.neighbours_data_path)
        self.till_end = constant.GRID_SIZE[0] * constant.GRID_SIZE[1]
        self.wfc_grid = _map.grid.copy()
        for i in range(len(self.wfc_grid)):
            for j in range(len(self.wfc_grid[0])):
                self.wfc_grid[i][j] = WCFTile(i, j, self.tile_types.tile_type_name_set)
        self.tile_types = tile_types

    def end_collapse(self) -> bool:
        return self.till_end == 0

    def collapse_cell(self, cell: WCFTile):
        cell.tile_type = self.find_best_option(cell.options)
        cell.collapsed = True
        self.till_end -= 1

    @staticmethod
    def find_best_option(options: [str]) -> str:
        return max(options, key=lambda x: x[1])

    def find_best_cell(self) -> WCFTile:
        return min(self.wfc_grid, key=lambda tile: len(tile.options))

    def update_near_collapsed(self, cell: WCFTile):
        x = cell.row
        y = cell.col
        for i in range(-1, 2):
            for j in range(-1, 2):
                # można zapisać inaczej
                if not(i == 0 and j == 0):
                    options = self.neighbours_dict[self.wfc_grid[x][y].tile_type][(i+1)*3+(j+1)]
                    self.wfc_grid[x + i][y + j].update(options)

    def collapse_all(self):
        x = random.randint(0, len(self.wfc_grid))
        y = random.randint(0, len(self.wfc_grid[0]))
        cell = self.wfc_grid[x][y]
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
