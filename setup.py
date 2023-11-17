import random
import tkinter as tk
from PIL import ImageTk, Image

x = 20
y = 20
map_size = (x, y)
name = "window name"
f_names = ['trawa','drzwi','sciana','woda']
assets = []
def load_assets():
    for file in f_names:
        assets.append(ImageTk.PhotoImage(Image.open("map_assets/"+file+".png").resize((cell_size, cell_size))))

cell_size = 16
root = tk.Tk()
canvas = tk.Canvas(root, width=map_size[0] * cell_size, height=map_size[1] * cell_size, background='black')
canvas.pack()
s_1 = 1*cell_size
s_2 = 1*cell_size

load_assets()
for i in range(map_size[0]):
    for j in range(map_size[1]):
        canvas.create_image(i*cell_size, j*cell_size, anchor=tk.NW, image=assets[random.randint(0, 3)])

root.title("name")
root.iconbitmap("map_assets/drzwi.png")
my_label = tk.Label(root, text=name)
my_label.pack()
root.mainloop()
