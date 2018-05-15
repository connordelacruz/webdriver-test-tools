"""
webdriver_test_tools |release|

Subpackages
===========

Framework
---------

Packages used by the unit testing framework.

.. toctree::

    webdriver_test_tools.config
    webdriver_test_tools.pageobject
    webdriver_test_tools.testcase

Utilities
---------

Testing utilities.

.. toctree::

    webdriver_test_tools.data
    webdriver_test_tools.webdriver

Internal
--------

Internal packages for test generation, project file creation, and command line
interfaces.

.. toctree::

    webdriver_test_tools.__main__
    webdriver_test_tools.cmd
    webdriver_test_tools.common
    webdriver_test_tools.project

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

