from PIL import Image


class TileTypes:
    tile_type_dict: dict
    tile_type_name_set: set

    def __init__(self, tile_type_texture_path: str, tile_type_data_path: str, grid_size: (int, int)):
        with open(tile_type_data_path, 'r') as file:
            file.readline()
            data = file.readlines()
            data = [x[:-1].split(";") for x in data]

        tile_textures = []
        texture = Image.open(tile_type_texture_path)
        texture_width, texture_height = texture.size

        square_width, square_height = texture_width/grid_size[1], texture_height/grid_size[0]
        for row in range(grid_size[1]):
            for col in range(grid_size[0]):
                left = col * square_width
                upper = row * square_height
                right = left + square_width
                lower = upper + square_height

                tile_texture = texture.crop((left, upper, right, lower))

                if tile_texture.getbbox() is not None:
                    tile_textures.append(tile_texture)

        self.tile_type_dict = {}
        self.tile_type_name_set = set()
        for index, tile_data in enumerate(data):
            self.tile_type_dict[tile_data[0]] = (tile_data[1], tile_data[2], tile_textures[index])
            self.tile_type_name_set.add(tile_data[0])
