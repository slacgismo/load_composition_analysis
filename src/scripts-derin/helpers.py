import os
import pathlib

def path_adder(path, file):
    return os.path.join(path, pathlib.Path(file))
