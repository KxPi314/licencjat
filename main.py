import constant
import setup
import waveFunctionCollapse

if __name__ == '__main__':
    grid = waveFunctionCollapse.Grid()
    arr = grid.collapse_all()

    gui = setup.GUI(constant.GRID_SIZE, constant.GRID_SIZE, arr)


