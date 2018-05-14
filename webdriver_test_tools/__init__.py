# TODO: split toctree into primary and internal?
"""
|release|

Subpackages
-----------

.. toctree::

    webdriver_test_tools.cmd
    webdriver_test_tools.config
    webdriver_test_tools.data
    webdriver_test_tools.pageobject
    webdriver_test_tools.project
    webdriver_test_tools.testcase
    webdriver_test_tools.webdriver

"""
from . import config
from . import data
from . import project
from . import webdriver
from . import common
from . import cmd
from .__about__ import (
    __version__, __author__, __email__, __license__, __copyright__,
)

__all__ = [
    '__version__', '__author__', '__email__', '__license__', '__copyright__',
]

