import random
from enum import Enum
import constant

grid_size = constant.GRID_SIZE
cell_type_num = 5


def collapse():
    return 1


class CellTypes(Enum):
    blank = 0
    grass = 1
    water = 2
    wall = 3
    door = 4
    floor = 5


class Cell:
    def __init__(self):
        self.collapsed = False
        self.type = CellTypes.blank
        self.options = [
            CellTypes.grass,
            CellTypes.water,
            CellTypes.wall,
            CellTypes.door,
            CellTypes.floor
        ]

    def get_connection_list(self):
        if self.type == CellTypes.grass:
            return list([CellTypes.grass, CellTypes.water, CellTypes.wall])
        elif self.type == CellTypes.water:
            return list([CellTypes.grass, CellTypes.water])
        elif self.type == CellTypes.wall:
            return list([CellTypes.grass, CellTypes.door, CellTypes.wall, CellTypes.floor])
        elif self.type == CellTypes.door:
            return list([CellTypes.wall, CellTypes.floor, CellTypes.grass])
        elif self.type == CellTypes.floor:
            return list([CellTypes.wall, CellTypes.door, CellTypes.floor, CellTypes.floor, CellTypes.floor])


class Grid:
    def __init__(self):
        self.grid = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.end = grid_size * grid_size

    def end_collapse(self):
        return self.end == 0

    def collapse_cell(self, x, y):
        self.grid[x][y].type = self.grid[x][y].options[random.randint(0, len(self.grid[x][y].options) - 1)]
        self.grid[x][y].options = []
        self.grid[x][y].collapsed = True
        self.end -= 1

    def find_best(self):
        min_ = cell_type_num
        best = []
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                if len(self.grid[i][j].options) < min_ and not self.grid[i][j].collapsed:
                    best.clear()
                    best.append((i, j))
                    min_ = len(self.grid[i][j].options)
                elif len(self.grid[i][j].options) == min_:
                    best.append((i, j))
        return best[random.randint(0, len(best) - 1)]

    def update_near_collapsed(self, x, y):
        arr = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for (i, j) in arr:
            if i in range(0, grid_size) and j in range(0, grid_size) and not self.grid[i][j].collapsed:
                self.grid[i][j].options = list(set(self.grid[i][j].options) &
                                               set(self.grid[x][y].get_connection_list()))
                # if len(self.grid[i][j].options) == 1:
                #    self.collapse_cell(i, j)

    def collapse_all(self):
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        self.collapse_cell(x, y)
        self.update_near_collapsed(x, y)

        while not self.end_collapse():
            (best_x, best_y) = self.find_best()
            self.collapse_cell(best_x, best_y)
            self.update_near_collapsed(best_x, best_y)
        return self.grid

# zle sprawdza gdzie co możę być/ drzwi przy wodzie np.
