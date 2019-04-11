"""Page object classes.


This module imports :class:`webdriver_test_tools.pageobject.base.BasePage` and
:class:`webdriver_test_tools.pageobject.yaml.YAMLParsingPageObject`.


Main Modules
------------

.. toctree::

   webdriver_test_tools.pageobject.base
   webdriver_test_tools.pageobject.prototypes


Prototype Modules
-----------------

.. toctree::

   webdriver_test_tools.pageobject.form
   webdriver_test_tools.pageobject.modal
   webdriver_test_tools.pageobject.nav
   webdriver_test_tools.pageobject.webpage


Internal Modules
----------------

.. toctree::

   webdriver_test_tools.pageobject.yaml
   webdriver_test_tools.pageobject.utils

"""

# TODO: re-organize subpackage?
from . import utils
from .base import BasePage
from .yaml import YAMLParsingPageObject
from . import prototypes

