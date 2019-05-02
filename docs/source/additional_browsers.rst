================================
Testing with Additional Browsers
================================

.. contents::

Enabling additional browsers
============================

By default, tests are generated for Firefox and Chrome. Additional browsers can
be enabled in ``<test_package>/config/browser.py``. For example, to generate
test cases for Safari, set ``Browsers.SAFARI`` to ``True`` in 
``BrowserConfig.ENABLED_BROWSERS``: 


.. code-block:: python
    :caption: config/browser.py
    :emphasize-lines: 5

    class BrowserConfig(browser.BrowserConfig):
        ENABLED_BROWSERS = {
            Browsers.FIREFOX: True,
            Browsers.CHROME: True,
            Browsers.SAFARI: True,
            Browsers.IE: False,
            Browsers.EDGE: False,
            Browsers.CHROME_MOBILE: False,
        }


Skipping tests for certain browsers
===================================

Some browser drivers don't support certain features of the Selenium WebDriver
API. If a test method or class requires these features to run, drivers that lack
support for them will likely encounter errors leading to false failures. The
``WebDriverTestCase`` class provides utilities for skipping tests in certain
browsers for these instances.

Skipping browsers for test methods
----------------------------------

To skip test methods for specific browsers, use the
``@WebDriverTestTools.skipBrowsers()`` decorator method:

.. code-block:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        @WebDriverTestCase.skipBrowsers(Browsers.SAFARI)
        def test_safari_skip(self):
            ...

        @WebDriverTestCase.skipBrowsers(Browsers.IE, Browsers.EDGE)
        def test_ie_edge_skip(self):
            ...


Skipping browsers for test case classes
---------------------------------------

To skip an entire test case class, override ``WebDriverTestCase.SKIP_BROWSERS``
with a list of browser names to skip:

.. code-block:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        SKIP_BROWSERS = [Browsers.SAFARI, Browsers.IE,]


Valid browser names are declared as constants in the ``Browsers`` class, which
is imported from ``webdriver_test_tools.testcase``.


Enabling mobile browsers
========================

Test cases that emulate mobile browser layouts are also enabled in
``<test_package>/config/browser.py``. For example, to generate test cases for
Chrome emulating a mobile layout, set ``Browsers.CHROME_MOBILE`` to ``True`` in
``BrowserConfig.ENABLED_BROWSERS``: 


.. code-block:: python
    :caption: config/browser.py
    :emphasize-lines: 8

    class BrowserConfig(browser.BrowserConfig):
        ENABLED_BROWSERS = {
            Browsers.FIREFOX: True,
            Browsers.CHROME: True,
            Browsers.SAFARI: False,
            Browsers.IE: False,
            Browsers.EDGE: False,
            Browsers.CHROME_MOBILE: True,
        }


Skipping tests for mobile browsers
==================================

Responsive site layouts can change significantly on mobile viewports, so the
procedure for testing a feature may require different steps. The
``WebDriverTestCase`` class provides utilities for conditionally skipping tests
for mobile or non-mobile browsers.

Skipping mobile browsers
------------------------

Test methods
~~~~~~~~~~~~

To skip test methods for mobile browsers, use the ``@WebDriverTestTools.skipMobile()`` decorator method:

.. code-block:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        @WebDriverTestCase.skipMobile()
        def test_mobile_skip(self):
            ...


Test case classes
~~~~~~~~~~~~~~~~~

To skip an entire test case class, set ``WebDriverTestCase.SKIP_MOBILE`` to ``True``:

.. code-block:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        SKIP_MOBILE = True


Skipping non-mobile browsers
----------------------------

Utilities are also provided for running tests exclusively in mobile browsers.

Test methods
~~~~~~~~~~~~

To skip test methods for non-mobile browsers, use the
``@WebDriverTestTools.mobileOnly()`` decorator method:

.. code-block:: python

    class ExampleTestCase(WebDriverTestCase):
        ...
        @WebDriverTestCase.mobileOnly()
        def test_mobile_only(self):
            ...


Test case classes
~~~~~~~~~~~~~~~~~

To only use mobile browsers for a test case class, subclass
``WebDriverMobileTestCase``:

.. code-block:: python

    class ExampleMobileTestCase(WebDriverMobileTestCase):
        ...


Modify test steps for mobile browsers
=====================================

.. todo better title?

Tests can check at runtime if the browser is mobile using the
``WebDriverTestCase.is_mobile()`` method. This can be useful in instances where
the steps for a test might vary slightly on mobile browsers. 


Example
-------

Suppose we have a responsive navbar that collapses on mobile viewports, adding
the extra step of expanding the navigation menu before clicking on a link. We
can determine what page object class to use for the navbar and conditionally
click the expand button based on ``self.is_mobile()``:

.. code-block:: python
   :caption: test/navbar.py
   :emphasize-lines: 10,13-14

   ...
   from example_project.pages.navbar import PrimaryNav, MobilePrimaryNav
   ...

   class PrimaryNavTestCase(WebDriverTestCase):
      ...
      def test_navbar_links(self):
        """Click links on the primary nav"""
         # Use collapsible NavObject class for mobile browsers
         navbar = MobilePrimaryNav(self.driver) if self.is_mobile() else PrimaryNav(self.driver)
         for link in navbar.links:
            # Expand collapsed menu first in mobile
            if self.is_mobile():
               navbar.click_expand_button()
            with self.subTest('Click navbar link', link=link):
               expected_url = navbar.click_link(link)
               self.assertUrlChange(expected_url)


.. _headless-browsers:

Using headless browsers
=======================

By default, tests run using the browser's GUI. While it can be helpful to see
what's going on during test execution, loading and rendering the browser window
can be resource-intensive and slows down performance during test execution.

To improve performance, tests can be run in `headless browsers`_ using the
``--headless`` argument:

::

    python -m <test_package> <args> --headless

.. note::

    When using the ``--headless`` argument, tests will only be run with
    the following web drivers that support running in a headless environment:
    
        * `Chrome <https://developers.google.com/web/updates/2017/04/headless-chrome>`__
        * Chrome Mobile [Emulated]
        * `Firefox <https://developer.mozilla.org/en-US/Firefox/Headless_mode>`__

.. _headless browsers: https://en.wikipedia.org/wiki/Headless_browser




