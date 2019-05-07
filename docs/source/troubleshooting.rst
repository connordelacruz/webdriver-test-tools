=====================
Troubleshooting Tests
=====================

.. contents::

.. todo doc overview

Common Issues
=============

"Element is not clickable at point (x,y). Other element would receive the click"
--------------------------------------------------------------------------------

.. currentmodule:: webdriver_test_tools.webdriver.actions

.. todo Flesh out example? Explore other potential solutions?

You may run across errors saying **"Element is not clickable at point (x,y).
Other element would receive the click: <element>"**. This is often due to a
fixed element obstructing the element you're attempting to click, such as a
sticky navbar or violator.

The :mod:`webdriver.actions.scroll
<webdriver_test_tools.webdriver.actions.scroll>` submodule includes the
:func:`scroll.into_view_fixed_nav` function, which scrolls an element into view
relative to a fixed object that may obstruct it. For example, suppose we want to
click on ``button_element``, but it's obstructed by a fixed navbar
``nav_element``:

.. code-block:: python

   ...
   # Scroll element to the top of the screen, relative to the fixed nav
   scroll.into_view_fixed_nav(driver, button_element, nav_element)
   # Click the button 
   button_element.click()

Despite the name, this function is not limited to objects fixed to the top of
the screen. Setting the optional parameter ``align_to_top=False`` will scroll
the target element into view relative to a fixed element on the bottom of the
screen. E.g. suppose we want to click on ``button_element``, but it's obstructed
by ``violator_element`` which is fixed to the bottom of the screen:

.. code-block:: python

   ...
   # Scroll element to the bottom of the screen, relative to the violator
   scroll.into_view_fixed_nav(driver, button_element, violator_element,
                              align_to_top=False)
   # Click the button 
   button_element.click()

For more information, see the API documentation for
:func:`scroll.into_view_fixed_nav`.


Accounting for timeouts on slow sites or pages
----------------------------------------------

By default, :ref:`WebDriverTestCase assertion methods <assertion-methods>` wait
10 seconds for the expected condition to occur before failing. There are some
instances where the default assertion wait time might not be long enough for a
slower site or page, causing tests to timeout prematurely. This default time can
be overridden for a specific assertion, an entire test case, or for the entire
test project.


Set timeout for a single assertion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each of the :ref:`WebDriverTestCase assertion methods <assertion-methods>`
accepts an optional parameter ``wait_timeout``, which overrides the default
timeout for a single assertion. E.g.:

.. code-block:: python

   self.assertVisible(element_locator, wait_timeout=30)


Set default timeout for a test case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If there are many assertions in a test case that are timing out prematurely, you
can set the ``DEFAULT_ASSERTION_TIMEOUT`` attribute, which will be used as the
default timeout value for all assertions in that class. E.g.:

.. code-block:: python

   class SlowPageTestCase(WebDriverTestCase):
      """Example test of a slow page"""
      SITE_URL = config.SiteConfig.SLOW_PAGE_URL
      # Set the default timeout for this class to 30 seconds
      DEFAULT_ASSERTION_TIMEOUT = 30

      def test_something(self):
         """Test a thing"""
         ...
         # Will wait 30 seconds
         self.assertExists(element_locator)

      def test_something_else(self):
         """Test another thing"""
         ...
         # Will wait 30 seconds
         self.assertInvisible(element_locator)
         # wait_timeout parameter takes precedence
         self.assertUrlChange(expected_url, wait_timeout=10)


Set default timeout for entire test project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also set the default timeout for all test cases in a project by setting
``WebDriverConfig.DEFAULT_ASSERTION_TIMEOUT``. E.g.:

.. code-block:: python
   :caption: <test_package>/config/webdriver.py

   class WebDriverConfig(config.WebDriverConfig):
      ...
      DEFAULT_ASSERTION_TIMEOUT = 30

As mentioned previously, this default can be overridden per-test case and
per-assertion.


Issues with specific browser drivers
------------------------------------

Browser-specific WebDrivers occasionally have bugs or quirks specific to them.
You may notice that a test is failing in a specific browser due to an exception
raised by the driver, rather than an assertion failing, which may be a sign that
your test is using a feature that isn't working or is handled differently in
that browser. 

Driver-specific issues can be difficult to pinpoint. If the test failure is only
happening for a certain browser, or you notice a pattern of tests failing in a
browser with similar exceptions, it can be useful to research that issue and see
if it's a known bug or if a workaround exists.

You may also want to check the links to each browser's Selenium driver in the
:ref:`driver table <driver-table>` to see if everything's up-to-date or if the
issue you're experiencing is documented.

If a workaround can't be found and the test failure seems to be a
browser-specific driver issue, you can skip these tests for the problem browser.
See :ref:`skip-browsers` for more info.


Tools for Debugging Tests
=========================

Screenshots
-----------

When troubleshooting a test, it can be useful to take screenshots to get a
visual of the window during testing. This framework includes utilities for
taking screenshots on test failure or at arbitrary points of a test. See the
:ref:`screenshots` documentation for details.


Pausing test execution
----------------------

When troubleshooting, it can be helpful to pause test execution at certain
points review things step-by-step. A simple way to insert a pause is using
Python's :func:`input` function. This function is meant to be used to prompt for
user input, but it can also be used to pause a test until hitting 'Enter',
allowing you to look at the browser window before continuing. E.g.:

.. code-block:: python

   ...
   def test_pause_example(self):
      ...
      # This will pause test execution until you hit enter
      # NOTE: you don't need to pass any parameters to input, this is just what
      # will be printed to standard output
      input('Paused')
      ...


Reporting an Issue with webdriver_test_tools
============================================

If the issue you're encountering appears to be with ``webdriver_test_tools``
specifically (rather than with Selenium or a specific browser driver), you can
report the issue on GitHub. **Before creating the issue:**

   * Check the open `GitHub Issues`_ to see if the issue has already been
     reported
   * If the issue hasn't been reported yet but appears to be related to
     Selenium, check `Selenium's GitHub Issues`_ to see if the issue has already
     been reported

If the issue isn't reported there and appears to be specific to WebDriver Test
Tools, `open a new issue`_ and fill out the required details, being as specific
as possible.

.. _Github Issues: https://github.com/connordelacruz/webdriver-test-tools/issues
.. _Selenium's GitHub Issues: https://github.com/SeleniumHQ/selenium/issues
.. _open a new issue: https://github.com/connordelacruz/webdriver-test-tools/issues/new?template=bug_report.md

