import constant
import setup
from map_elements import Map
from textures_and_data import TileTypes

if __name__ == '__main__':
    tile_types = TileTypes("map_assets/v.3/Island_24x24.png", "map_assets_data/v.3/pond.csv", (8, 9))
    print(len(tile_types.tile_type_dict))
    _map = Map('inny')
    for i in range(6):
        temp = []
        for j in range(1, 9):
            if tile_types.tile_type_dict.get(str((i*7+j)))[2] is not None:
                temp.append(tile_types.tile_type_dict.get(str((i*8+j)))[2])

        _map.grid.append(temp)
    gui = setup.GUI(_map)
