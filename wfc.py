import random
import numpy as np
from map_elements import TileType, Direction, Map, Tile


class Wfc:
    neighbors_dict: dict

    def __init__(self, _map: Map, t_types: [TileType]):
        self.neighbors_dict = {}
        self.t_types = t_types
        self.build_neighbors_dict(t_types)
        self._map = _map
        self.collapse_counter = self._map.grid_size[0] * self._map.grid_size[1]
        self._map.grid = [[Tile(row, col, t_types) for col in range(self._map.grid_size[1])] for row in
                          range(self._map.grid_size[0])]

    def define_starting_platforms(self):
        self._map.grid[0][0] = Tile(
            0,
            0,
            self.t_types,
            tile_type=self.t_types[0]
        )

        self._map.grid[-1][-1] = Tile(
            self._map.grid_size[0],
            self._map.grid_size[1],
            self.t_types,
            tile_type=self.t_types[0]
        )

        self._map.grid[0][0].collapsed = True
        self._map.grid[0][0].options = []
        self.collapse_counter -= 1
        self.update_near_collapsed(0, 0)

        self._map.grid[-1][-1].collapsed = True
        self._map.grid[-1][-1].options = []
        self.collapse_counter -= 1
        self.update_near_collapsed(self._map.grid_size[0]-1, self._map.grid_size[1]-1)

    def collapse_all(self):
        x = random.randint(0, self._map.grid_size[0]-1)
        y = random.randint(0, self._map.grid_size[1] - 1)

        self.collapse_cell(x, y)
        self.update_near_collapsed(x, y)
        self.define_starting_platforms()
        while not self.end_collapse():
            next_cell = self.find_best_cell()
            x, y = next_cell
            self.collapse_cell(x, y)

    def end_collapse(self):
        if self.collapse_counter <= 0:
            return True
        return False

    def collapse_cell(self, row, col):
        self._map.grid[row][col].tile_type = self.best_cell_option(row, col)
        self._map.grid[row][col].walkable = self._map.grid[row][col].tile_type.walkable
        self._map.grid[row][col].collapsed = True
        self._map.grid[row][col].options = []
        self.collapse_counter -= 1
        self.update_near_collapsed(row, col)

    def best_cell_option(self, row, col) -> TileType or None:
        if self._map.grid[row][col].options:
            return random.choice(self._map.grid[row][col].options)
        return None

    def find_best_cell(self) -> (int, int):
        best = []
        for row in range(0, self._map.grid_size[0]):
            for col in range(0, self._map.grid_size[1]):
                if not self._map.grid[row][col].collapsed:
                    if not best:
                        best = [(row, col)]
                    elif len(self._map.grid[row][col].options) < len(self._map.grid[best[0][0]][best[0][1]].options):
                        best = [(row, col)]
                    elif len(self._map.grid[row][col].options) == len(self._map.grid[best[0][0]][best[0][1]].options):
                        best.append((row, col))
        return random.choice(best)

    def update_near_collapsed(self, row, col):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not(i == 0 and j == 0) and 0 <= row+i < self._map.grid_size[0] and 0 <= col+j < self._map.grid_size[1]:
                    if not self._map.grid[row+i][col+j].collapsed:
                        direction = Direction.x_y_to_direction(i, j)
                        if self._map.grid[row][col].tile_type is None:
                            new_options = self.t_types
                        else:
                            new_options = self.neighbors_dict[self._map.grid[row][col].tile_type][direction]
                        self._map.grid[row+i][col+j].update(new_options)
                        if len(self._map.grid[row+i][col+j].options) == 1:
                            self.collapse_cell(row+i, col+j)

    def draw_test(self):
        for row in range(self._map.grid_size[0]):
            for col in range(self._map.grid_size[1]):
                if row == 0:
                    self._map.grid[row][col] = Tile(row, col, self.t_types, tile_type=self.t_types[0])
                elif row == 0:
                    self._map.grid[row][col] = Tile(
                        row,
                        col,
                        self.t_types,
                        tile_type=random.choice(self.neighbors_dict[self._map.grid[row][col].tile_type][Direction.Right])
                    )
                else:
                    up = self.neighbors_dict[self._map.grid[row-1][col].tile_type][Direction.Down]
                    left = self.neighbors_dict[self._map.grid[row-1][col].tile_type][Direction.Right]
                    options = list(set(up) & set(left))

                    self._map.grid[row][col] = Tile(
                        row,
                        col,
                        self.t_types,
                        tile_type=random.choice(up)
                    )

    def build_neighbors_dict(self, t_types: [TileType]):
        for current_type in t_types:
            self.neighbors_dict[current_type] = {}
            for direction in Direction:
                options = [t for t in t_types
                           if np.array_equal(
                               t.puzzle_edge(direction.opposite()),
                               current_type.puzzle_edge(direction)
                           )
                           ]
                self.neighbors_dict[current_type][direction] = options
