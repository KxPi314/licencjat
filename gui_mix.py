import tkinter as tk
import constant as const
from PIL import ImageTk, Image


class Gui:
    # Edit values
    tile_selection: bool
    tile_position: (int, int)
    direction: int or None
    tiles: list
    tiles_neighbours: dict
    direction_button_actions: dict
    tk_image: Image

    # Build values

    def __init__(self):
        self.root: tk = tk.Tk()
        self.WINDOW_NAME = "Map_generation"
        self.root.title(self.WINDOW_NAME)
        self.root.geometry("%sx%s" % (const.WINDOW_SIZE[0], const.WINDOW_SIZE[1]))
        self.build_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)
        self.setup_build_frame()
        self.setup_edit_frame()
        self.edit_frame.pack(fill=tk.BOTH, expand=True)
        self.root.mainloop()

    def change_build_to_edit(self):
        self.build_frame.forget()
        self.edit_frame.pack(fill=tk.BOTH, expand=True)

    def change_edit_to_build(self):
        self.edit_frame.forget()
        self.build_frame.pack(fill=tk.BOTH, expand=True)

    # Build Frame functions
    def setup_build_frame(self):

        # Values
        image_references = []

        # Frames
        button_frame = tk.Frame(self.build_frame, bg='gray')

        # Widgets
        canvas = tk.Canvas(self.build_frame, background='black')

        listbox = tk.Listbox(button_frame, bg='grey', height=3)
        listbox.insert(1, 'WFC')
        listbox.insert(1, 'algorytm2')
        listbox.insert(1, 'algorytm3')

        new_map_button = tk.Button(button_frame, text="new map", command=self.build_button1, width=15)
        a_star_button = tk.Button(button_frame, text="A star", command=self.build_button2, width=15)
        save_button = tk.Button(button_frame, text="save", command=self.build_button3, width=15)
        edit_button = tk.Button(button_frame, text="edit", command=self.change_build_to_edit, width=15)

        text = tk.StringVar()
        text.set("wynik: 0")
        score = tk.Label(button_frame, textvariable=text)

        # Packing
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        new_map_button.pack()
        a_star_button.pack()
        save_button.pack()
        edit_button.pack()
        score.pack()
        listbox.pack()

    def build_button1(self):
        # alg = self.listbox.get??
        # uruchom algorytm
        self.build_load_map_texture()

    def build_button2(self):
        print("Button 2 clicked")

    def build_button3(self):
        print("Button 3 clicked")

    def build_button4(self):
        print("Button 4 clicked")

    def build_load_map_texture(self):
        pass
    # def load_map_texture(self):
    #     canvas_width = constant.GRID_SIZE[0] * constant.TILE_SIZE[0]
    #     canvas_height = constant.GRID_SIZE[1] * constant.TILE_SIZE[1]
    #     self.canvas.config(width=canvas_width, height=canvas_height)
    #
    #     for i in range(len(self._map.grid)):
    #         for j in range(len(self._map.grid[0])):
    #             if self._map.grid[i][j] is not None:
    #                 pil_image = self.tile_types.tile_type_dict.get(self._map.grid[i][j].tile_type)
    #                 resized_image = pil_image.resize(
    #                     (constant.TILE_SIZE[0], constant.TILE_SIZE[1])
    #                 )
    #                 tk_image = ImageTk.PhotoImage(resized_image)
    #                 self.canvas.create_image(
    #                     j * constant.TILE_SIZE[0],
    #                     i * constant.TILE_SIZE[1],
    #                     anchor=tk.NW,
    #                     image=tk_image
    #                 )
    #
    #                 self.image_references.append(tk_image)

    # Edit Frame functions
    def setup_edit_frame(self):
        self.tile_selection = False
        self.tile_position = None
        self.direction = None
        self.tiles = []
        self.tiles_neighbours = {}
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
        self.tk_image = ImageTk.PhotoImage(img.resize((500, 500)))

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

        canvas = tk.Canvas(self.edit_frame,
                           background='Black')
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

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
        canvas.create_image(250, 250, image=self.tk_image)
        canvas.bind('<Button-1>', self.tile_clicked)

    def edit_back(self):
        print("back button pressed")

    def edit_save(self):
        print("sace button pressed")

    def direction_button_action(self, value: int):
        print("button: ", value)
        # if center button pressed
        if value == 4:
            self.tile_selection = True
            self.tile_position = None
            self.direction = None
        else:
            self.direction = value

    def tile_clicked(self, event):
        x = int(event.x / (self.tk_image.width() / 9))
        y = int(event.y / (self.tk_image.height() / 8))
        print(x, y)
        # if tile_selection:
        #     tile_position = (x,y)
        #     if tiles_neighbours.get(tile_position) is None:
        #         tiles_neighbours[tile_position] = {}
        #     return
        # elif direction is not None:
        #     tiles_neighbours[tile_position][direction] = (x, y)


g = Gui()
