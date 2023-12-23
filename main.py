import gui_mix
from map_elements import Map
from textures_and_data import TileTypes

if __name__ == '__main__':
    # ładowanie elementów mapy
    tile_types = TileTypes("map_assets/v.3/Island_24x24.png", "map_assets_data/v.3/pond.csv", (8, 9))
    # utworzenie pustej mapy
    _map = Map()
    gui = gui_mix.Gui(_map, tile_types)
