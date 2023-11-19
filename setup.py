import waveFunctionCollapse
import constant
import tkinter as tk
from PIL import ImageTk, Image


class GUI():
    def __init__(self, x, y, grid):
        self.grid = grid
        self.map_grid_size = (x, y)
        self.map_cell_size = constant.MAP_CELL_SIZE
        self.window_name = "window name"
        self.assets = []
        self.assets_names = ['trawa', 'drzwi', 'sciana', 'woda']
        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            self.root,
            width=self.map_grid_size[0] * self.map_cell_size,
            height=self.map_grid_size[1] * self.map_cell_size, background='black'
        )
        self.load_map()
        self.canvas.pack()
        self.root.title(self.window_name)
        self.root.iconbitmap("map_assets/drzwi.png")
        self.root.mainloop()

    def load_map(self):
        self.load_map_assets()
        for i in range(self.map_grid_size[0]):
            for j in range(self.map_grid_size[1]):
                choice = 0
                if self.grid[i][j].type == waveFunctionCollapse.CellTypes.grass:
                    choice = 0
                elif self.grid[i][j].type == waveFunctionCollapse.CellTypes.water:
                    choice = 3
                elif self.grid[i][j].type == waveFunctionCollapse.CellTypes.wall:
                    choice = 2
                elif self.grid[i][j].type == waveFunctionCollapse.CellTypes.door:
                    choice = 1
                self.canvas.create_image(
                    i * self.map_cell_size,
                    j * self.map_cell_size,
                    anchor=tk.NW,
                    image=self.assets[choice]
                )

    def load_map_assets(self):
        for file in self.assets_names:
            self.assets.append(
                ImageTk.PhotoImage(
                    Image.open("map_assets/" + file + ".png")
                    .resize((self.map_cell_size, self.map_cell_size))
                )
            )