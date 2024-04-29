import random
import tkinter as tk
from PIL import ImageTk, Image

import Astar
from map_elements import Map, TileType, Direction
import constant
from new_wfc import wfcRunner
import numpy as np


class App:
    tile_img_dict: dict

    # Edit values
    asset_image: Image
    tk_asset_image: Image
    edit_img_scale: (int, int)
    edit_canvas: tk.Canvas
    edit_work_state: str
    tile_img_size: (int, int)
    selected_tiles: dict
    properties_walkable: dict
    selected_bitmap: dict
    bitmap_id_input: tk.Text
    bitmap_color_id = dict
    edit_tile_set_size: (int, int)
    edit_tile_size: (float, float)
    t_types: [TileType]
    checkbox_var: tk.IntVar
    tile_bitmap_shape: (int, int)
    edit_id_list: tk.Listbox

    # Build values
    map_image = Image
    tk_map_image = tk.Image
    build_canvas: tk.Canvas
    map_grid_size: (int, int)
    grid_width_box: tk.Text
    grid_height_box: tk.Text

    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_state('zoomed')
        self.root.title("Wave Function Collapse map generator")
        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()
        # BUDOWANIE
        self.t_types = []
        self.tile_img_dict = {}
        self.tile_bitmap_shape = (2, 2)
        # ---------

        self.build_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)
        # bazowo rozmiar mapy zapisany jako 10 na 18
        self.map_grid_size = (10, 18)

        self.setup_build_frame()
        self.setup_edit_frame()

        # wypełniam mapę pustymi kafelkami
        self._map = Map(self.map_grid_size)
        # ustawaim tryb okienka bazowo na tryb budowania
        self.build_frame.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def change_build_to_edit(self):
        self.build_frame.forget()
        self.edit_frame.pack(fill=tk.BOTH, expand=True)

    def change_edit_to_build(self):
        self.edit_frame.forget()
        self.build_frame.pack(fill=tk.BOTH, expand=True)

    # Build Frame functions
    # w nich nic ciekawego tylko rozstawienie guzików i pól
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
        self.grid_width_box.insert("1.0", str(self.map_grid_size[1]))
        self.grid_height_box.insert("1.0", str(self.map_grid_size[0]))

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
            # odczyt rozmiaru mapy podanego przez uzytkownika
            self.build_get_grid_size()
            # wywołanie wfc w cpp
            wfcRunner(build_neighbors_dict(self.t_types), self.map_grid_size[1], self.map_grid_size[0])
            self.build_load_map_texture()

    def build_a_star(self):
        try:
            start = (0, 0)
            target = (self._map.grid_size[0] - 1, self._map.grid_size[1] - 1)
            path = Astar.a_star_path(start, target, self._map)
            scale = (self.map_image.size[0] / self.map_grid_size[1], self.map_image.size[1] / self.map_grid_size[0])
            offset = (
            self.map_image.size[0] / self.map_grid_size[1] / 2, self.map_image.size[1] / self.map_grid_size[0] / 2)
            for index, element in enumerate(path):
                if index + 1 < len(path):
                    first_point = (element[1] * scale[0] + offset[0], element[0] * scale[1] + offset[1])
                    second_point = (
                        path[index + 1][1] * scale[0] + offset[0], path[index + 1][0] * scale[1] + offset[1])
                    self.build_canvas.create_line(first_point, second_point)
        except AttributeError:
            print("A* Error")

    def build_save(self):
        if self.map_image is not None:
            self.map_image.save("saves/new_map.jpg")

    def build_get_grid_size(self):
        x = self.grid_width_box.get("1.0", tk.END).strip()
        y = self.grid_height_box.get("1.0", tk.END).strip()
        if y.isdecimal() and x.isdecimal():
            self.map_grid_size = (int(y), int(x))
            self._map = Map(self.map_grid_size)
        return self.map_grid_size

    def build_load_map_texture(self):
        map_image = Image.new(
            "RGB",
            (
                constant.TILE_SIZE[1] * self.map_grid_size[1],
                constant.TILE_SIZE[0] * self.map_grid_size[0]
            )
        )
        with open("out.txt") as wfc_output:
            try:
                for i, line in enumerate(wfc_output):
                    for j, elem in enumerate(line.split(" ")):
                        if elem != '\n' and int(elem) != 0:
                            tile_image = self.tile_img_dict[self.t_types[int(elem)-1].img_id]
                            tile_image = tile_image.resize((constant.TILE_SIZE[0], constant.TILE_SIZE[1]))
                            map_image.paste(tile_image, (constant.TILE_SIZE[0] * j, constant.TILE_SIZE[1] * i))
            except Exception as e:
                print(e)
            wfc_output.close()

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
        self.properties_walkable = {}
        self.selected_bitmap = {}
        self.bitmap_color_id = {}
        self.checkbox_var = tk.IntVar()
        self.checkbox_var.set(2)

        # Frames
        main_frame = tk.Frame(self.edit_frame)
        button_frame = tk.Frame(main_frame)
        bitmap_frame = tk.Frame(main_frame)
        checkbox_frame = tk.Frame(main_frame)

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

        bitmap_shape_check_3_3 = tk.Checkbutton(checkbox_frame, text='3/3',
                                                command=self.edit_bitmap_shape, variable=self.checkbox_var,
                                                onvalue=3, offvalue=2)

        bitmap_shape_check_2_2 = tk.Checkbutton(checkbox_frame, text='2/2',
                                                command=self.edit_bitmap_shape, variable=self.checkbox_var,
                                                onvalue=2, offvalue=3)

        self.edit_id_list = tk.Listbox(main_frame, width=20)

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
        bitmap_shape_check_3_3.pack()
        bitmap_shape_check_2_2.pack()
        checkbox_frame.pack()
        self.edit_id_list.pack()
        properties_button.pack()

        # loading img
        self.edit_canvas.create_image(
            self.tk_asset_image.width() / 2,
            self.tk_asset_image.height() / 2,
            image=self.tk_asset_image
        )
        self.edit_canvas.bind('<Button-1>', self.tile_clicked)

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
                top_b = (left + self.edit_tile_size[0] / 3, up)
                left_b = (left, up + self.edit_tile_size[1] / 3)
                right_b = (right, up + self.edit_tile_size[1] / 3)
                bottom_b = (left + self.edit_tile_size[0] / 3, down)

                top_left = (left, up)
                top_right = (right, up)
                bottom_left = (left, down)
                bottom_right = (right, down)

                # for (3/3)
                top_bit = False
                left_bit = False
                right_bit = False
                bottom_bit = False

                top_left_bit = False
                top_right_bit = False
                bottom_left_bit = False
                bottom_right_bit = False

                puzzle_shape = np.zeros(self.tile_bitmap_shape)

                # Check if each corner is in selected_bitmap
                for x in self.selected_bitmap.keys():
                    if self.tile_bitmap_shape == (2, 2):
                        if (x[0], x[1]) == top_left:
                            top_left_bit = self.selected_bitmap[x][1]
                        elif (x[2], x[1]) == top_right:
                            top_right_bit = self.selected_bitmap[x][1]
                        elif (x[0], x[3]) == bottom_left:
                            bottom_left_bit = self.selected_bitmap[x][1]
                        elif (x[2], x[3]) == bottom_right:
                            bottom_right_bit = self.selected_bitmap[x][1]
                    if self.tile_bitmap_shape == (3, 3):
                        if (x[0], x[1]) == top_left:
                            top_left_bit = self.selected_bitmap[x][1]
                        elif (x[2], x[1]) == top_right:
                            top_right_bit = self.selected_bitmap[x][1]
                        elif (x[0], x[3]) == bottom_left:
                            bottom_left_bit = self.selected_bitmap[x][1]
                        elif (x[2], x[3]) == bottom_right:
                            bottom_right_bit = self.selected_bitmap[x][1]
                        elif (x[0], x[1]) == top_b:
                            top_bit = self.selected_bitmap[x][1]
                        elif (x[0], x[1]) == left_b:
                            left_bit = self.selected_bitmap[x][1]
                        elif (x[2], x[1]) == right_b:
                            right_bit = self.selected_bitmap[x][1]
                        elif (x[0], x[3]) == bottom_b:
                            bottom_bit = self.selected_bitmap[x][1]

                if self.tile_bitmap_shape == (2, 2):
                    puzzle_shape = np.array([
                        [top_left_bit, top_right_bit],
                        [bottom_left_bit, bottom_right_bit]
                    ])
                elif self.tile_bitmap_shape == (3, 3):
                    puzzle_shape = np.array([
                        [top_left_bit, top_bit, top_right_bit],
                        [left_bit, 0, right_bit],
                        [bottom_left_bit, bottom_bit, bottom_right_bit]
                    ])

                walkable = False
                if tile_pos in self.properties_walkable.keys():
                    walkable = True
                t_type = TileType(index, puzzle_shape, walkable)
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
        self.edit_canvas.create_image(
            self.tk_asset_image.width() / 2,
            self.tk_asset_image.height() / 2,
            image=self.tk_asset_image
        )
        for tile in self.properties_walkable:
            new_id = self.edit_canvas.create_rectangle(
                tile,
                outline="grey",
                fill="green",
                stipple="gray50",
                width=2
            )
            self.properties_walkable[tile] = new_id
        self.edit_work_state = "properties"

    def edit_bitmap_shape(self):
        if self.checkbox_var.get() == 3:
            self.tile_bitmap_shape = (3, 3)
        else:
            self.tile_bitmap_shape = (2, 2)

    def edit_get_bitmap_color(self, color_id: int) -> str:
        if color_id in self.bitmap_color_id.keys():
            return self.bitmap_color_id[color_id]
        hex_numbers = [str(hex(random.randint(17, 255))[2:]) for _ in range(3)]
        new_color = "#" + hex_numbers[0] + hex_numbers[1] + hex_numbers[2]
        self.bitmap_color_id[color_id] = new_color
        self.edit_id_list.insert(0, str(color_id) + ": " + new_color)
        self.edit_id_list.itemconfig(0, {'fg': new_color})
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
            if self.edit_work_state == "properties":
                x = int(event.x / self.edit_tile_size[0])
                y = int(event.y / self.edit_tile_size[1])
                rect_position = (
                    x * self.edit_tile_size[0],
                    y * self.edit_tile_size[1],
                    x * self.edit_tile_size[0] + self.edit_tile_size[0],
                    y * self.edit_tile_size[1] + self.edit_tile_size[1]
                )
                if rect_position in self.properties_walkable.keys():
                    self.edit_canvas.delete(self.properties_walkable.get(rect_position))
                    self.properties_walkable.pop(rect_position, None)
                else:
                    rect_id = self.edit_canvas.create_rectangle(
                        rect_position,
                        outline="grey",
                        fill="green",
                        stipple="gray50",
                        width=2
                    )
                    self.properties_walkable[rect_position] = rect_id
            if self.edit_work_state == "bitmap" and self.bitmap_id_input.get("1.0", tk.END).strip().isdecimal():
                bit_tile_size = (
                    self.edit_tile_size[0] / self.tile_bitmap_shape[0],
                    self.edit_tile_size[1] / self.tile_bitmap_shape[1]
                )
                x = int(event.x / (bit_tile_size[0]))
                y = int(event.y / (bit_tile_size[1]))

                rect_position = (
                    x * bit_tile_size[0],
                    y * bit_tile_size[1],
                    x * bit_tile_size[0] + bit_tile_size[0],
                    y * bit_tile_size[1] + bit_tile_size[1]
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


def build_neighbors_dict(t_types: [TileType]):
    directions = [Direction.LeftUP, Direction.Up, Direction.RightUp,
                  Direction.Left, Direction.Right,
                  Direction.LeftDown, Direction.Down, Direction.RightDown]
    neighbors_dict = {}
    #dodawanie zera / służy ono za puste pole
    all_types = []
    for num_0 in range(len(t_types)):
        all_types.append(num_0+1)
    neighbors_dict[0] = []
    for _ in Direction:
         neighbors_dict[0].append(all_types)
    #dodawanie pozostałych wartosci
    for num, current_type in enumerate(t_types):
        neighbors_dict[num+1] = []
        for direction in directions:
            direction_arr = []
            for num_2, t in enumerate(t_types):
                if np.array_equal(t.puzzle_edge(direction.opposite()), current_type.puzzle_edge(direction)):
                    direction_arr.append(num_2+1)
            neighbors_dict[num+1].append(direction_arr)
    print(neighbors_dict)
    return neighbors_dict
