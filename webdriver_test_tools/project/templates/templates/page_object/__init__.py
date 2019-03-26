# This file is only so python recognizes the parent directory and is not a template file
import os

def get_path():
    """Returns the path of this template directory"""
    return os.path.dirname(os.path.abspath(__file__))

