from enum import Enum
import numpy as np


class Direction(Enum):
    Up = 1
    Down = -1
    Left = 2
    Right = -2
    LeftUP = 3
    RightDown = -3
    RightUp = 4
    LeftDown = -4

    def opposite(self):
        return Direction(-self.value)

    @staticmethod
    def x_y_to_direction(x, y):
        if x == -1 and y == -1:
            return Direction.LeftUP
        elif x == -1 and y == 0:
            return Direction.Up
        elif x == -1 and y == 1:
            return Direction.RightUp
        elif x == 0 and y == -1:
            return Direction.Left
        elif x == 0 and y == 0:
            return None
        elif x == 0 and y == 1:
            return Direction.Right
        elif x == 1 and y == -1:
            return Direction.LeftDown
        elif x == 1 and y == 0:
            return Direction.Down
        else:
            return Direction.RightDown


class TileType:
    img_id: int
    puzzle_shape: np.array
    walkable: bool

    def __init__(self, img_id, puzzle_shape, walkable):
        self.img_id = img_id
        self.puzzle_shape = puzzle_shape
        self.walkable = walkable

    def puzzle_edge(self, direction: Direction):
        result = None
        if direction == Direction.Up:
            result = self.puzzle_shape[0]
        elif direction == Direction.Down:
            result = self.puzzle_shape[-1]
        elif direction == Direction.Left:
            result = self.puzzle_shape[:, 0]
        elif direction == Direction.Right:
            result = self.puzzle_shape[:, -1]
        elif direction == Direction.LeftUP:
            result = self.puzzle_shape[0, 0]
        elif direction == Direction.RightUp:
            result = self.puzzle_shape[0, -1]
        elif direction == Direction.LeftDown:
            result = self.puzzle_shape[-1, 0]
        else:
            result = self.puzzle_shape[-1, -1]
        return result


class Tile:
    row: int
    col: int
    walkable: bool
    tile_type: TileType

    # wfc data
    options: [TileType]

    def __init__(self, row, col, start_options, tile_type=None, walkable=True):
        self.row = row
        self.col = col
        self.collapsed = False
        self.walkable = walkable
        self.options = start_options
        self.tile_type = tile_type


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

    def walkable_land(self):
        count = 0
        for row in self.grid:
            for tile in row:
                if tile is not None and tile.walkable:
                    count += 1
        return count