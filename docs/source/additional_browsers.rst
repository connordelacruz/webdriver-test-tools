Testing with Additional Browsers
================================

.. contents::

Enabling additional browsers
----------------------------

By default, tests are generated for Firefox and Chrome. Additional browsers can be enabled in ``<test_package>/config/browser.py``. For example, to generate test cases for Safari, add ``Browsers.SAFARI`` to ``BrowserConfig.BROWSER_TEST_CLASSES``: 

``config/browser.py``:

.. code:: python
    
    from webdriver_test_tools.classes.webdriver_test_case import *
    from webdriver_test_tools.config import browser


    class BrowserConfig(browser.BrowserConfig):
        # Dictionary of usable test case classes indexed by the short name for that class (i.e. its command line argument)
        BROWSER_TEST_CLASSES = {
            Browsers.FIREFOX: FirefoxTestCase,
            Browsers.CHROME: ChromeTestCase,
            Browsers.SAFARI: SafariTestCase,
            # Browsers.IE: IETestCase,
            # Browsers.EDGE: EdgeTestCase,
        }


Skipping tests for certain browsers
-----------------------------------

Some browser drivers don't support certain features of the Selenium WebDriver API. If a test method or class requires these features to run, drovers that lack support for them will likely encounter errors leading to false failures. The ``WebDriverTestCase`` class provides utilities for skipping tests in certain browsers for these instances.

Skipping browsers for test methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To skip test methods for specific browsers, use the ``@WebDriverTestTools.skipBrowsers()`` decorator method:

.. code:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        @WebDriverTestCase.skipBrowsers(Browsers.SAFARI)
        def test_safari_skip(self):
            ...

        @WebDriverTestCase.skipBrowsers(Browsers.IE, Browsers.EDGE)
        def test_ie_edge_skip(self):
            ...


Skipping browsers for test case classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To skip an entire test case class, override ``WebDriverTestCase.SKIP_BROWSERS`` with a list of browser names to skip:

.. code:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        SKIP_BROWSERS = [Browsers.SAFARI, Browsers.IE,]


Valid browser names are declared as constants in the ``Browsers`` class, which is imported from ``webdriver_test_tools.classes.webdriver_test_case``


