class Pixel:
    pass


class Quark:
    slice: [[Pixel]]
    indexes: (int, int)
    neighbours: [[]]

    def __init__(self, map_slice: [[Pixel]]):
        self.slice = map_slice
        self.indexes = []
        self.neighbours = [None for x in range(8)]


class WFC:
    quark_array: [[Quark]]
    # Tworzy słownik wycinków i indeksów w których się pojawiają

    def __init__(self, bitmap, slice_size):
        map_size = len(bitmap) / slice_size
        self.quark_map = [[None for _ in map_size] for _ in map_size]
        self.quark_dict = {}
        self.map_slice_arr = [[]]

    def read_bitmap(self, bitmap: [[Pixel]], slice_size: (int, int)):
        for y in range(len(bitmap) / slice_size):
            self.map_slice_arr.append([])
            for x in range(len(bitmap) / slice_size):
                map_slice = bitmap[y * slice_size:y * slice_size + slice_size] \
                    [x * slice_size:x * slice_size + slice_size]
                self.map_slice_arr[y].append(Quark(map_slice))
        for y in range(len(self.map_slice_arr)):
            for x in range(len(self.map_slice_arr)):
                self.map_slice_arr[y][x].indexes = (y, x)
                for idx, n in enumerate(self.map_slice_arr[y-1:y+1][x-1:x+1]):
                    if n in self.map_slice_arr and n.index != (y, x):
                        self.map_slice_arr[y][x].neighbours[idx].append(n)
        #teraz znajdz te same tile mapy i dodaj sąsiadów

    def load_quarks_map(self):
        pass
        

    #używa indeksów i zapisuje listy przyległych z danego kierunku
    def add_neighbours(self):
        pass


