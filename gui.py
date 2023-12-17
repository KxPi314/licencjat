from PIL import ImageTk
import tkinter as tk
from map_elements import Map
from textures_and_data import TileTypes
import constant


class GUI:
    _map: Map
    tile_types: TileTypes

    def __init__(self, _map: Map, tile_types: TileTypes):
        self.window_name = "map_generation"
        self.root = tk.Tk()
        self._map = _map
        self.tile_types = tile_types

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=constant.GRID_SIZE[1] * constant.TILE_SIZE[1],
            height=constant.GRID_SIZE[0] * constant.TILE_SIZE[0],
            background='black'
        )
        self.canvas.pack(side=tk.LEFT)
        self.image_references = []

        button_frame = tk.Frame(self.root, bg='gray', padx=10, pady=10)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        button1 = tk.Button(button_frame, text="Button 1", command=self.button1_action)
        button2 = tk.Button(button_frame, text="Button 2", command=self.button2_action)
        button3 = tk.Button(button_frame, text="Button 3", command=self.button3_action)
        button4 = tk.Button(button_frame, text="Button 4", command=self.button4_action)

        # Pack buttons
        button1.pack(pady=5)
        button2.pack(pady=5)
        button3.pack(pady=5)
        button4.pack(pady=5)

        # Window title and main loop
        self.root.title(self.window_name)
        self.root.mainloop()

    def button1_action(self):
        print("Button 1 clicked")
        self.load_map_texture()

    def button2_action(self):
        print("Button 2 clicked")

    def button3_action(self):
        print("Button 3 clicked")

    def button4_action(self):
        print("Button 4 clicked")

    def load_map_texture(self):
        canvas_width = constant.GRID_SIZE[0] * constant.TILE_SIZE[0]
        canvas_height = constant.GRID_SIZE[1] * constant.TILE_SIZE[1]
        self.canvas.config(width=canvas_width, height=canvas_height)

        for i in range(len(self._map.grid)):
            for j in range(len(self._map.grid[0])):
                if self._map.grid[i][j] is not None:
                    pil_image = self.tile_types.tile_type_dict.get(self._map.grid[i][j].tile_type)
                    resized_image = pil_image.resize(
                        (constant.TILE_SIZE[0], constant.TILE_SIZE[1])
                    )
                    tk_image = ImageTk.PhotoImage(resized_image)
                    self.canvas.create_image(
                        j * constant.TILE_SIZE[0],
                        i * constant.TILE_SIZE[1],
                        anchor=tk.NW,
                        image=tk_image
                    )

                    # Keep a reference to avoid garbage collection
                    self.image_references.append(tk_image)
