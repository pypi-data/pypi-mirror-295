import os
import ctypes

# Get the path to the .so file relative to this file
_so_file = os.path.join(os.path.dirname(__file__), 'deepan_regression_tool.cpython-39-x86_64-linux-gnu.so')

# Load the .so file using ctypes
deepan_regression_tool = ctypes.CDLL(_so_file)