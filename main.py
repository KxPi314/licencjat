import random

import constant
import setup
import waveFunctionCollapse
import functools

if __name__ == '__main__':

    list_a = [random.random()-0.5 for _ in range(1000)]


    # read template
    # pass template to bild wave
    grid = waveFunctionCollapse.Grid()
    arr = grid.collapse_all()
    gui = setup.GUI(constant.GRID_SIZE, constant.GRID_SIZE, arr)
    gui.load_map()


