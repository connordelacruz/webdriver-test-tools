from . import project_root
from . import package_root
from . import config
from . import templates
from . import tests
from . import log
# For retrieving the template file path
import os

def get_path():
    """Returns the path of this template directory"""
    return os.path.dirname(os.path.abspath(__file__))

