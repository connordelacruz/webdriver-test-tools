# TODO: Explain subpackage organization (primary vs internal)
# TODO: Categorize into Framework, Utility, and Internal instead?
# TODO: document __main__ and __about__?
"""
webdriver_test_tools |release|

Subpackages
===========

Primary
-------

.. toctree::

    webdriver_test_tools.config
    webdriver_test_tools.data
    webdriver_test_tools.pageobject
    webdriver_test_tools.testcase
    webdriver_test_tools.webdriver

Internal
--------

.. toctree::

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

