import random
import tkinter as tk

from PIL import ImageTk, Image
from map_elements import Map, TileType
import constant
from wfc import Wfc
import numpy as np


class Gui:
    tile_bitmap_shape: (int, int)
    tile_img_dict: dict

    # Edit values
    asset_image: Image
    tk_asset_image: Image
    edit_img_scale: (int, int)
    edit_canvas: tk.Canvas
    edit_work_state: str
    tile_img_size: (int, int)
    selected_tiles: dict
    selected_bitmap: dict
    bitmap_id_input: tk.Text
    bitmap_color_id = dict
    edit_tile_set_size: (int, int)
    edit_tile_size: (float, float)
    t_types: [TileType]

    # Build values
    map_image = Image
    tk_map_image = tk.Image
    build_canvas: tk.Canvas
    grid_size: (int, int)
    grid_width_box: tk.Text
    grid_height_box: tk.Text

    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_state('zoomed')
        self.root.title("Map_generation")
        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()
        self.t_types = []
        self.tile_img_dict = {}
        self.tile_bitmap_shape = (3, 3)

        self.build_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)

        self.setup_build_frame()
        self.setup_edit_frame()

        self.grid_size = (10, 10)
        self._map = Map(self.grid_size)

        self.build_frame.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def change_build_to_edit(self):
        self.build_frame.forget()
        self.edit_frame.pack(fill=tk.BOTH, expand=True)

    def change_edit_to_build(self):
        self.edit_frame.forget()
        self.build_frame.pack(fill=tk.BOTH, expand=True)

    # Build Frame functions
    def setup_build_frame(self):

        # Frames
        button_frame = tk.Frame(self.build_frame, bg='gray')
        height_frame = tk.Frame(button_frame, bg='gray')
        width_frame = tk.Frame(button_frame, bg='gray')

        # Widgets
        self.build_canvas = tk.Canvas(self.build_frame, background='black')

        grid_width_label = tk.Label(width_frame, text="x:", width=2, height=1)
        grid_height_label = tk.Label(height_frame, text="y:", width=2, height=1)
        self.grid_width_box = tk.Text(width_frame, width=12, height=1)
        self.grid_height_box = tk.Text(height_frame, width=12, height=1)
        new_map_button = tk.Button(button_frame, text="new map", command=self.build_new_map, width=16)
        a_star_button = tk.Button(button_frame, text="A star", command=self.build_a_star, width=16)
        save_button = tk.Button(button_frame, text="save", command=self.build_save, width=16)
        edit_button = tk.Button(button_frame, text="edit", command=self.change_build_to_edit, width=16)

        text = tk.StringVar()
        text.set("score: 0")
        score = tk.Label(button_frame, textvariable=text)

        # Packing
        self.build_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        width_frame.pack()
        height_frame.pack()
        grid_height_label.pack(side=tk.LEFT)
        grid_width_label.pack(side=tk.LEFT)
        self.grid_width_box.pack()
        self.grid_height_box.pack()
        new_map_button.pack()
        a_star_button.pack()
        save_button.pack()
        edit_button.pack()
        score.pack()

    def build_new_map(self):
        if self.tile_img_dict != {}:
            self.build_canvas.delete("all")
            self.build_get_grid_size()
            wfc = Wfc(self._map, self.t_types)
            wfc.collapse_all()
            self.build_load_map_texture()

    def build_a_star(self):
        pass

    def build_save(self):
        if self.map_image is not None:
            self.map_image.save("saves/new_map.jpg")

    def build_get_grid_size(self):
        x = self.grid_width_box.get("1.0", tk.END).strip()
        y = self.grid_height_box.get("1.0", tk.END).strip()
        if y.isdecimal() and x.isdecimal():
            self.grid_size = (int(y), int(x))
            self._map = Map(self.grid_size)
        return self.grid_size

    def build_load_map_texture(self):
        map_image = Image.new(
            "RGB",
            (
                constant.TILE_SIZE[1] * self.grid_size[1],
                constant.TILE_SIZE[0] * self.grid_size[0]
            )
        )
        for i in range(0, self.grid_size[0]):
            for j in range(0, self.grid_size[1]):
                if self._map.grid[i][j] is not None and self._map.grid[i][j].tile_type is not None:
                    tile_image = self.tile_img_dict[self._map.grid[i][j].tile_type.img_id]
                    tile_image = tile_image.resize((constant.TILE_SIZE[0], constant.TILE_SIZE[1]))
                    map_image.paste(tile_image, (constant.TILE_SIZE[0] * j, constant.TILE_SIZE[1] * i))

        original_width, original_height = map_image.size
        ratio = original_width / original_height

        canvas_width = self.edit_canvas.winfo_width()
        canvas_height = self.edit_canvas.winfo_height()

        if canvas_width / canvas_height > ratio:
            new_height = canvas_height
            new_width = int(canvas_height * ratio)
        else:
            new_width = canvas_width
            new_height = int(canvas_width / ratio)

        self.map_image = map_image.resize((new_width, new_height), box=(0, 0, map_image.width, map_image.height))

        self.tk_map_image = ImageTk.PhotoImage(self.map_image)
        self.build_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_map_image)
        self.build_canvas.update_idletasks()

    # Edit Frame functions
    def setup_edit_frame(self):
        self.edit_img_scale = 2
        self.asset_image = Image.open('map_assets/v.3/Island_24x24.png')
        self.tk_asset_image = ImageTk.PhotoImage(
            self.asset_image.resize((
                self.asset_image.width * self.edit_img_scale,
                self.asset_image.height * self.edit_img_scale
            )))

        # Values
        button_size = (10, 1)
        self.edit_work_state = "select_tile"
        self.tile_img_size = (24, 24)
        self.selected_tiles = {}
        self.selected_bitmap = {}
        self.bitmap_color_id = {}

        # Frames
        main_frame = tk.Frame(self.edit_frame)
        button_frame = tk.Frame(main_frame)
        bitmap_frame = tk.Frame(main_frame)

        # Widgets
        save_button = tk.Button(master=button_frame,
                                command=self.edit_save,
                                text='save',
                                width=7,
                                height=button_size[1])
        back_button = tk.Button(master=button_frame,
                                command=self.change_edit_to_build,
                                text='back',
                                width=7,
                                height=button_size[1])

        select_button = tk.Button(master=main_frame,
                                  command=self.edit_select_tile,
                                  text='select tiles',
                                  width=16,
                                  height=button_size[1])

        bitmap_button = tk.Button(master=main_frame,
                                  command=self.edit_bitmap,
                                  text='bitmap',
                                  width=16,
                                  height=button_size[1])

        properties_button = tk.Button(master=main_frame,
                                      command=self.edit_properties,
                                      text='properties',
                                      width=16,
                                      height=button_size[1])

        bitmap_id_label = tk.Label(bitmap_frame, text="id:", width=2, height=1)
        self.bitmap_id_input = tk.Text(master=bitmap_frame,
                                       width=12,
                                       height=button_size[1])

        self.edit_canvas = tk.Canvas(self.edit_frame, background='Black')
        # Packing

        self.edit_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_frame.pack()
        button_frame.pack()
        save_button.pack(side=tk.LEFT)
        back_button.pack()
        select_button.pack()
        bitmap_button.pack()
        bitmap_id_label.pack(side=tk.LEFT)
        self.bitmap_id_input.pack()
        bitmap_frame.pack()
        properties_button.pack()

        # loading img
        self.edit_canvas.create_image(
            self.tk_asset_image.width() / 2,
            self.tk_asset_image.height() / 2,
            image=self.tk_asset_image
        )
        self.edit_canvas.bind('<Button-1>', self.tile_clicked)


# fix to (3*3)
    def edit_save(self):
        if self.selected_tiles != {}:
            self.tile_img_dict = {}
            self.t_types = []

            for index, tile_pos in enumerate(self.selected_tiles.keys()):
                left, up, right, down = tile_pos

                tile_texture = self.asset_image.crop(
                    (left / self.edit_img_scale,
                     up / self.edit_img_scale,
                     right / self.edit_img_scale,
                     down / self.edit_img_scale)
                )

                self.tile_img_dict[index] = tile_texture

                top_left = (left, up)
                top_right = (right, up)
                bottom_left = (left, down)
                bottom_right = (right, down)

                top_left_bit = False
                top_right_bit = False
                bottom_left_bit = False
                bottom_right_bit = False
                # Check if each corner is in selected_bitmap
                for x in self.selected_bitmap.keys():
                    if (x[0], x[1]) == top_left:
                        position = (x[0], x[1], x[0] + self.edit_tile_size[1] / 2, x[1] + self.edit_tile_size[1] / 2)
                        top_left_bit = self.selected_bitmap[position][1]
                    elif (x[2], x[1]) == top_right:
                        position = (x[2] - self.edit_tile_size[0] / 2, x[1], x[2], x[1] + self.edit_tile_size[1] / 2)
                        top_right_bit = self.selected_bitmap[position][1]
                    elif (x[0], x[3]) == bottom_left:
                        position = (x[0], x[3] - self.edit_tile_size[1] / 2, x[0] + self.edit_tile_size[0] / 2, x[3])
                        bottom_left_bit = self.selected_bitmap[position][1]
                    elif (x[2], x[3]) == bottom_right:
                        position = (x[2] - self.edit_tile_size[0] / 2, x[3] - self.edit_tile_size[1] / 2, x[2], x[3])
                        bottom_right_bit = self.selected_bitmap[position][1]

                # Create a TileType object and append it to t_types

                puzzle_shape = np.array([
                    [top_left_bit, top_right_bit],
                    [bottom_left_bit, bottom_right_bit]
                ])

                t_type = TileType(index, puzzle_shape)
                self.t_types.append(t_type)

    def edit_select_tile(self):
        self.edit_canvas.delete("all")
        self.edit_canvas.create_image(
            self.tk_asset_image.width() / 2,
            self.tk_asset_image.height() / 2,
            image=self.tk_asset_image
        )
        for tile in self.selected_tiles:
            new_id = self.edit_canvas.create_rectangle(
                tile,
                outline="grey",
                fill="green",
                stipple="gray50",
                width=2
            )
            self.selected_tiles[tile] = new_id
        self.edit_work_state = "select_tile"

    def edit_bitmap(self):
        self.edit_canvas.delete("all")
        self.edit_canvas.create_image(
            self.tk_asset_image.width() / 2,
            self.tk_asset_image.height() / 2,
            image=self.tk_asset_image
        )
        for tile in self.selected_tiles:
            new_id = self.edit_canvas.create_rectangle(
                tile,
                outline="grey",
                fill="grey",
                stipple="gray50",
                width=2
            )
            self.selected_tiles[tile] = new_id
        for bit in self.selected_bitmap:
            color = self.edit_get_bitmap_color(self.selected_bitmap[bit][1])
            new_id = self.edit_canvas.create_rectangle(
                bit,
                outline="grey",
                fill=color,
                stipple="gray50",
                width=2
            )
            self.selected_bitmap[bit] = (new_id, self.selected_bitmap[bit][1])
        self.edit_work_state = "bitmap"

    def edit_properties(self):
        self.edit_canvas.delete("all")
        self.edit_canvas.create_image(250, 250, image=self.tk_asset_image)
        self.edit_work_state = "properties"

    def edit_get_bitmap_color(self, color_id: int) -> str:
        if color_id in self.bitmap_color_id.keys():
            return self.bitmap_color_id[color_id]
        hex_numbers = [str(hex(random.randint(17, 255))[2:]) for _ in range(3)]
        new_color = "#" + hex_numbers[0] + hex_numbers[1] + hex_numbers[2]
        self.bitmap_color_id[color_id] = new_color
        return new_color

    def tile_clicked(self, event):
        self.edit_tile_set_size = (9, 8)
        self.edit_tile_size = (
            (self.tk_asset_image.width() / self.edit_tile_set_size[0]),
            (self.tk_asset_image.height() / self.edit_tile_set_size[1])
        )
        if event.x < self.tk_asset_image.width() and event.y < self.tk_asset_image.height():
            if self.edit_work_state == "select_tile":
                x = int(event.x / self.edit_tile_size[0])
                y = int(event.y / self.edit_tile_size[1])
                rect_position = (
                    x * self.edit_tile_size[0],
                    y * self.edit_tile_size[1],
                    x * self.edit_tile_size[0] + self.edit_tile_size[0],
                    y * self.edit_tile_size[1] + self.edit_tile_size[1]
                )
                if rect_position in self.selected_tiles.keys():
                    self.edit_canvas.delete(self.selected_tiles.get(rect_position))
                    self.selected_tiles.pop(rect_position, None)
                else:
                    rect_id = self.edit_canvas.create_rectangle(
                        rect_position,
                        outline="grey",
                        fill="green",
                        stipple="gray50",
                        width=2
                    )
                    self.selected_tiles[rect_position] = rect_id
            # fix (3*3)
            if self.edit_work_state == "bitmap" and self.bitmap_id_input.get("1.0", tk.END).strip().isdecimal():
                half_tile_size = (self.edit_tile_size[0] / 2, self.edit_tile_size[1] / 2)
                x = int(event.x / (half_tile_size[0]))
                y = int(event.y / (half_tile_size[1]))

                rect_position = (
                    x * half_tile_size[0],
                    y * half_tile_size[1],
                    x * half_tile_size[0] + half_tile_size[0],
                    y * half_tile_size[1] + half_tile_size[1]
                )
                if rect_position in self.selected_bitmap.keys():
                    self.edit_canvas.delete(self.selected_bitmap.get(rect_position)[0])
                    self.selected_bitmap.pop(rect_position, None)
                else:
                    rect_id = self.edit_canvas.create_rectangle(
                        rect_position,
                        outline="grey",
                        fill=self.edit_get_bitmap_color(int(self.bitmap_id_input.get("1.0", tk.END).strip())),
                        stipple="gray50",
                        width=2
                    )
                    self.selected_bitmap[rect_position] = (rect_id,
                                                           int(self.bitmap_id_input.get("1.0", tk.END).strip()))
