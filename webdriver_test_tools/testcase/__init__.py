"""Web driver test case classes.

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

