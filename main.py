from gui import Gui
import pickle
import os


def save_gui_state(gui_object, path_):
    with open(path_, 'wb') as f:
        pickle.dump(gui_object, f)


def load_gui_state(path_):
    with open(path_, 'rb') as f:
        gui_object = pickle.load(f)
    return gui_object


if __name__ == '__main__':
    gui = None
    try:
        gui = load_gui_state("gui_saves/gui_state.pkl")
    except Exception as a:
        print(a)
        gui = Gui()
    try:
        save_gui_state(gui, "gui_saves")
    except Exception as a:
        print(a)

# TO DO
#nie sprawdzam czy pierwszy jest walkable
