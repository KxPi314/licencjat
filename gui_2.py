import tkinter as tk
import constant as const

from PIL import Image, ImageTk

#trzeba z tego zrobić jedną klasę z gui bo teraz jest problem ze zmiennymi

tile_selection: bool = False
tile_position: (int, int) = None
direction: int or None = None
tiles = []
tiles_neighbours = {}

def back():
    print("back button pressed")


def save():
    print("sace button pressed")


def direction_button_action(value: int):
    pass


direction_button_actions = {
    0: lambda: direction_button_action(0),
    1: lambda: direction_button_action(1),
    2: lambda: direction_button_action(2),
    3: lambda: direction_button_action(3),
    4: lambda: direction_button_action(4),
    5: lambda: direction_button_action(5),
    6: lambda: direction_button_action(6),
    7: lambda: direction_button_action(7),
    8: lambda: direction_button_action(8),
}
WINDOW_NAME = "Tile Build"

root: tk = tk.Tk()
#root.config(bg='darkgrey')
root.title(WINDOW_NAME)
IMAGE = Image.open('map_assets/v.3/Island_24x24.png')
TK_IMAGE = ImageTk.PhotoImage(IMAGE.resize((500, 500)))
root.geometry("%sx%s" % (const.WINDOW_SIZE[0], const.WINDOW_SIZE[1]))

# values
button_size = (10, 1)
dir_button_size = (6, 3)
listbox_size = (int(button_size[0]*2.5)+1, dir_button_size[1]*4)



def tile_clicked(event):
    x = int(event.x / (TK_IMAGE.width() / 9))
    y = int(event.y / (TK_IMAGE.height() / 8))
    if tile_selection:
        tile_position = (x,y)
        if tiles_neighbours.get(tile_position) is None:
            tiles_neighbours[tile_position] = {}
        return
    elif direction is not None:
        tiles_neighbours[tile_position][direction] = (x,y)


# Frames
main_frame = tk.Frame()
button_frame = tk.Frame(main_frame)
direction_frame = tk.Frame(main_frame)
direction_frames = [tk.Frame(direction_frame) for _ in range(3)]

# widgets
save_button = tk.Button(master=button_frame, command=save, text='save', width=button_size[0], height=button_size[1])
back_button = tk.Button(master=button_frame, command=back, text='back',width=button_size[0], height=button_size[1])


canvas = tk.Canvas(root, background='Black')
listbox = tk.Listbox(main_frame, width=listbox_size[0], height=listbox_size[1])

buttons = []
for i in range(9):
    if i != 4:
        buttons.append(tk.Button(master=direction_frames[int(i/3)],
                                 command=direction_button_actions.get(i),
                                 width=dir_button_size[0], height=dir_button_size[1])
                       )
    else:
        buttons.append(tk.Button(master=direction_frames[int(i / 3)],
                                 command=direction_button_actions.get(i),
                                 background='lightblue', activebackground='#1e629e',
                                 width=dir_button_size[0], height=dir_button_size[1])
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
canvas.create_image(250, 250, image=TK_IMAGE)
canvas.bind('<Button-1>', tile_clicked)
root.mainloop()


def direction_button_action(value: int):
    print("button: ", value)
    if value == 4:
        tile_selection = True
        tile_position = None
        direction = None
    else:
        direction = value

