from PIL import Image
import tkinter as tk

image = Image.open('Grass.png')
crop_box = (16,0,32,16)
image = image.crop(crop_box)
image.save('tile1.png')

def load_and_display_image():
    # Provide the path to your cropped image
    cropped_img_path = 'tile1.png'
    root = tk.Tk()
    tk_image = tk.PhotoImage(file=cropped_img_path)
    label = tk.Label(root, image=tk_image)
    label.pack()
    root.mainloop()

load_and_display_image()



#pobierz zdj
#zapisz jako zmienne
#użyj wygenerowanej mapy
#zklej zdj za pomocą assetów. wyświetl
#zapisz pdf