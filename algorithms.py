import random
from map_elements import Tile


class WFC:
    neighbours_dict: dict
    grid: [[Tile]]

    def __init__(self, _map, name_set, grid_size, neighbours_dict):
        self._map = _map
        self.name_set = name_set
        self.grid_size = grid_size

        self.neighbours_dict = neighbours_dict
        self.till_end = self.grid_size[0] * self.grid_size[1]
        self.grid = _map.grid.copy()
        self.bonus_tile = Tile(0, 0, name_set)
        arr = list(name_set)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j] = Tile(i, j, name_set)
                self.grid[i][j].tile_type_name = random.choice(name_set)
                self.grid[i][j].collapsed = True
        #self.collapse_all()
        _map.grid = self.grid

    def collapse_all(self):
        x = random.randint(0, self.grid_size[0]-1)
        y = random.randint(0, self.grid_size[1]-1)
        while not self.end_collapse():
            self.collapse_cell(self.grid[x][y])
            self.update_near_collapsed(self.grid[x][y])
            cell = self.find_best_cell()
            x = cell.row
            y = cell.col

    def end_collapse(self) -> bool:
        return self.till_end <= 0

    def collapse_cell(self, cell: Tile):
        x = cell.row
        y = cell.col
        self.grid[x][y].tile_type_name = self.find_best_option(self.grid[x][y].options)
        self.grid[x][y].collapsed = True
        self.till_end -= 1


    @staticmethod
    def find_best_option(options: [str]) -> str:
        return max(options, key=lambda x: x[1])

    def find_best_cell(self) -> Tile:
        best = self.bonus_tile
        arr = []
        for row in self.grid:
            for cell in row:
                if not cell.collapsed:
                    if len(cell.options) < len(best.options):
                        best = cell
                        arr = [best]
                    elif len(cell.options) == len(best.options):
                        arr.append(cell)
        if arr:
            return random.choice(arr)
        return best

    def update_near_collapsed(self, cell: Tile):
        x = cell.row
        y = cell.col
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # można zapisać inaczej
                if not (i == 0 and j == 0) and 0 < (x + i) < self.grid_size[0] and 0 < (y + j) < self.grid_size[1]:
                    options = self.neighbours_dict[self.grid[x][y].tile_type_name][counter]
                    counter += 1
                    self.grid[x + i][y + j].update(options)
