class Pixel:
    name: str

class Tile:
    def __init__(self, img):
        self.img = img
        self.up = []
        self.down = []
        self.right = []
        self.left = []

class Quark:
    slice: [[Pixel]]

    def __init__(self, map_slice: [[Pixel]]):
        self.slice = map_slice
        self.indexes = []
        self.neighbours = [[] for x in range(8)]


class WFC: