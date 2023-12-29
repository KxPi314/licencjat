import tkinter as tk
from PIL import ImageTk, Image
from map_elements import Map
from textures_and_data import TileTypes
import constant
import algorithms


class Gui:
    # Edit values
    tile_selection: bool
    tile_name: str or None
    direction: int or None
    tiles: list
    tiles_neighbours: dict
    direction_button_actions: dict
    tk_map_image: Image
    edit_canvas: tk.Canvas
    neighbours: list

    # Build values
    build_canvas: tk.Canvas
    grid_size: (int, int)
    grid_width_box: tk.Text
    grid_height_box: tk.Text

    def __init__(self, tile_types: TileTypes):
        self.map_image = None
        self.selection_rect = None
        self.grid_size = (10, 10)
        self._map = Map(self.grid_size)
        self.tile_types = tile_types
        self.image_references = []
        self.root: tk = tk.Tk()
        self.WINDOW_NAME = "Map_generation"
        self.root.title(self.WINDOW_NAME)
        self.root.geometry("%sx%s" % (constant.WINDOW_SIZE[0], constant.WINDOW_SIZE[1]))
        self.build_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)
        self.setup_build_frame()
        self.setup_edit_frame()
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

        listbox = tk.Listbox(button_frame, bg='grey', height=3)
        listbox.insert(1, 'WFC')
        listbox.insert(1, 'algorytm2')
        listbox.insert(1, 'algorytm3')

        grid_width_label = tk.Label(width_frame, text="x:", width=2, height=1)
        grid_height_label = tk.Label(height_frame, text="y:", width=2, height=1)
        self.grid_width_box = tk.Text(width_frame, width=12, height=1)
        self.grid_height_box = tk.Text(height_frame, width=12, height=1)
        new_map_button = tk.Button(button_frame, text="new map", command=self.build_new_map, width=16)
        a_star_button = tk.Button(button_frame, text="A star", command=self.build_a_star, width=16)
        save_button = tk.Button(button_frame, text="save", command=self.build_save, width=16)
        edit_button = tk.Button(button_frame, text="edit", command=self.change_build_to_edit, width=16)

        text = tk.StringVar()
        text.set("wynik: 0")
        score = tk.Label(button_frame, textvariable=text)

        # Packing
        self.build_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        height_frame.pack()
        width_frame.pack()
        grid_height_label.pack(side=tk.LEFT)
        grid_width_label.pack(side=tk.LEFT)
        self.grid_height_box.pack()
        self.grid_width_box.pack()
        new_map_button.pack()
        a_star_button.pack()
        save_button.pack()
        edit_button.pack()
        score.pack()
        listbox.pack()

    def build_new_map(self):
        self.build_canvas.delete("all")
        self.tile_types.tile_type_name_set = \
            [x for x in self.tile_types.tile_type_name_set if x in self.tiles_neighbours]
        self.build_get_grid_size()
        wfc = algorithms.WFC(self._map, self.tile_types, self.grid_size)
        wfc.neighbours_dict = self.tiles_neighbours
        self.build_load_map_texture()

    @staticmethod
    def build_a_star():
        print("Button 2 clicked")

    def build_save(self):
        if self.map_image is not None:
            self.map_image.save("saves/new_map.jpg")

    def build_get_grid_size(self):
        x = self.grid_width_box.get("1.0", tk.END).strip()
        y = self.grid_height_box.get("1.0", tk.END).strip()
        if y.isdecimal() and x.isdecimal():
            self.grid_size = (int(x), int(y))
            self._map = Map(self.grid_size)
        return self.grid_size

    def build_load_map_texture(self):
        map_image = Image.new("RGB", (constant.TILE_SIZE[0]*self.grid_size[0], constant.TILE_SIZE[1]*self.grid_size[1]))
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self._map.grid[i][j].tile_type_name is not None:
                    tile_image = self.tile_types.tile_type_dict.get(self._map.grid[i][j].tile_type_name)[2]
                    tile_image = tile_image.resize((constant.TILE_SIZE[0], constant.TILE_SIZE[1]))
                    if tile_image is not None:
                        map_image.paste(tile_image, (constant.TILE_SIZE[0]*i, constant.TILE_SIZE[1]*j))
        if self.grid_size[0] > self.grid_size[1]:
            self.map_image = map_image.resize(
                (constant.CANVAS_SIZE[0],
                 int(constant.CANVAS_SIZE[1] * (self.grid_size[1]/self.grid_size[0])))
            )
        else:
            self.map_image = map_image.resize(
                (int(constant.CANVAS_SIZE[0] * (self.grid_size[0] / self.grid_size[1])),
                 constant.CANVAS_SIZE[1])
            )
        self.tk_map_image = ImageTk.PhotoImage(self.map_image)
        self.build_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_map_image)

    # Edit Frame functions
    def setup_edit_frame(self):
        self.tile_selection = False
        self.tile_name = None
        self.direction = None
        self.tiles = []
        self.tiles_neighbours = {}
        self.neighbours = []
        self.direction_button_actions = {
            0: lambda: self.direction_button_action(0),
            1: lambda: self.direction_button_action(1),
            2: lambda: self.direction_button_action(2),
            3: lambda: self.direction_button_action(3),
            4: lambda: self.direction_button_action(4),
            5: lambda: self.direction_button_action(5),
            6: lambda: self.direction_button_action(6),
            7: lambda: self.direction_button_action(7),
            8: lambda: self.direction_button_action(8),
        }
        img = Image.open('map_assets/v.3/Island_24x24.png')
        self.tk_map_image = ImageTk.PhotoImage(img.resize((500, 500)))
        self.selection_rect = None

        # Values
        button_size = (10, 1)
        dir_button_size = (6, 3)
        listbox_size = (int(button_size[0] * 2.5) + 1, dir_button_size[1] * 4)

        # Frames
        main_frame = tk.Frame(self.edit_frame)
        button_frame = tk.Frame(main_frame)
        direction_frame = tk.Frame(main_frame)
        direction_frames = [tk.Frame(direction_frame) for _ in range(3)]

        # Widgets
        save_button = tk.Button(master=button_frame,
                                command=self.edit_save,
                                text='save',
                                width=button_size[0],
                                height=button_size[1])
        back_button = tk.Button(master=button_frame,
                                command=self.change_edit_to_build,
                                text='back',
                                width=button_size[0],
                                height=button_size[1])

        self.edit_canvas = tk.Canvas(self.edit_frame, background='Black')
        listbox = tk.Listbox(main_frame,
                             width=listbox_size[0],
                             height=listbox_size[1])

        buttons = []
        for i in range(9):
            if i != 4:
                buttons.append(tk.Button(master=direction_frames[int(i / 3)],
                                         command=self.direction_button_actions.get(i),
                                         width=dir_button_size[0],
                                         height=dir_button_size[1])
                               )
            else:
                buttons.append(tk.Button(master=direction_frames[int(i / 3)],
                                         command=self.direction_button_actions.get(i),
                                         background='lightblue',
                                         activebackground='#1e629e',
                                         width=dir_button_size[0],
                                         height=dir_button_size[1])
                               )

        # Packing

        self.edit_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_frame.pack()
        button_frame.pack()
        save_button.pack(side=tk.LEFT)
        back_button.pack()

        direction_frame.pack()
        direction_frames[0].pack()
        direction_frames[1].pack()
        direction_frames[2].pack()
        for index, button in enumerate(buttons):
            button.pack(side=tk.LEFT)

        listbox.pack()

        # loading img
        self.edit_canvas.create_image(250, 250, image=self.tk_map_image)
        self.edit_canvas.bind('<Button-1>', self.tile_clicked)

    def edit_save(self):
        print(self.neighbours)

    def direction_button_action(self, value: int):
        if self.direction is not None:
            for elem in self.neighbours[self.direction]:
                self.edit_canvas.delete(elem)
        # if center button pressed
        if value == 4:
            self.tile_selection = True
            self.tile_name = None
            self.direction = None
        else:
            self.tile_selection = False
            self.direction = value
            for elem in self.neighbours[self.direction]:
                self.edit_canvas.move(elem)

    def tile_clicked(self, event):
        x = int(event.x / (self.tk_map_image.width() / 9))
        y = int(event.y / (self.tk_map_image.height() / 8))
        if self.tile_selection:
            self.neighbours = [[] for _ in range(9)]
            self.edit_canvas.delete(self.selection_rect)
            self.selection_rect = self.edit_canvas.create_rectangle((self.tk_map_image.width() / 9) * x,
                                                                    (self.tk_map_image.height() / 8) * y,
                                                                    (self.tk_map_image.width() / 9) * (x + 1),
                                                                    (self.tk_map_image.height() / 8) * (y + 1),
                                                                    fill='red', outline='', stipple='gray50')
            self.edit_canvas.move(self.selection_rect, 0, 0)
            self.tile_name = str(x) + ',' + str(y)
            if self.tiles_neighbours.get(self.tile_name) is None:
                self.tiles_neighbours[self.tile_name] = [[] for _ in range(9)]
            return
        elif self.direction is not None and self.tile_name is not None:
            rec = self.edit_canvas.create_rectangle((self.tk_map_image.width() / 9) * x,
                                                    (self.tk_map_image.height() / 8) * y,
                                                    (self.tk_map_image.width() / 9) * (x + 1),
                                                    (self.tk_map_image.height() / 8) * (y + 1),
                                                    fill='green', outline='', stipple='gray50')
            self.edit_canvas.move(rec, 0, 0)
            self.neighbours[self.direction].append(rec)
            if str(x) + ',' + str(y) not in self.tiles_neighbours[self.tile_name][self.direction]:
                self.tiles_neighbours[self.tile_name][self.direction].append(str(x) + ',' + str(y))
            else:
                self.tiles_neighbours[self.tile_name][self.direction].remove(str(x) + ',' + str(y))


# poprawa estetyki kodu
# zapis słownika w pickle
# load map_texture wymaga pracy
# i wfc też
