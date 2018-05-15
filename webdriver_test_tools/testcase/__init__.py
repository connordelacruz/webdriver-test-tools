"""Web driver test case classes.

This module imports the following classes:

    :class:`webdriver_test_tools.testcase.webdriver.WebDriverTestCase`
    :class:`webdriver_test_tools.testcase.webdriver.WebDriverMobileTestCase`
    :class:`webdriver_test_tools.testcase.browsers.Browsers`

Main Modules
------------

.. toctree::

   webdriver_test_tools.testcase.webdriver
   webdriver_test_tools.testcase.browsers


Browser Test Case Modules
-------------------------

.. toctree::

   webdriver_test_tools.testcase.chrome
   webdriver_test_tools.testcase.edge
   webdriver_test_tools.testcase.firefox
   webdriver_test_tools.testcase.ie
   webdriver_test_tools.testcase.safari

"""

from .webdriver import WebDriverTestCase, WebDriverMobileTestCase
from .browsers import Browsers

