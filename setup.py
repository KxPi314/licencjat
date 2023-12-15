from map_elements import Map
import constant
import tkinter as tk
from PIL import ImageTk, Image


class GUI:
    _map: Map

    def __init__(self, _map: Map):
        self.window_name = "map"
        self.root = tk.Tk()

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=constant.GRID_SIZE[1] * constant.TILE_SIZE[1],
            height=constant.GRID_SIZE[0] * constant.TILE_SIZE[0],
            background='black'
        )
        self.canvas.pack(side=tk.LEFT)

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
        for i in range(constant.GRID_SIZE[0]):
            for j in range(constant.GRID_SIZE[1]):
                self.canvas.create_image(
                    i * constant.TILE_SIZE[0],
                    j * constant.TILE_SIZE[1],
                    anchor=tk.NW,
                    image=self._map.grid[i][j].tile_type
                )

