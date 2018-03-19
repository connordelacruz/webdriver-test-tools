=============================
Selenium WebDriver Test Tools
=============================

Utilities for writing front-end test suites using `Selenium WebDriver <https://www.seleniumhq.org/docs/03_webdriver.jsp>`__ and python unit tests.

.. contents::

Overview
========

This project aims to reduce the amount of time and additional code
required to automate front-end functional testing by providing utilities
and conventions for building test suites.

This project uses Selenium WebDriver for automated browser actions and the python unittest library for the test framework. 

Prerequisites
=============

Python
------

-  python 3+
-  pip

Drivers
-------

Required
~~~~~~~~

The following web drivers are required:

-  `geckodriver <https://github.com/mozilla/geckodriver/releases>`__
   (FireFox)
-  `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__
   (Google Chrome)

On MacOS, both drivers can be installed using
`Homebrew <https://brew.sh/>`__:

::

    brew install geckodriver chromedriver

Platform-Specific (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project currently supports the following platform-specific drivers as well. These are not required, but can be useful for adding tests for platform-specific drivers:

-  `Safari <https://webkit.org/blog/6900/webdriver-support-in-safari-10/>`__ 
-  `Internet Explorer <https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver>`__
-  `Edge <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`__

.. note::

    These need to be enabled in ``<test_package>/config/browser.py`` by uncommenting 
    the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``.

.. warning::

    Support of these web drivers is experimental and may not work as expected. Some
    drivers are not fully compatible with Selenium's WebDriver API, so unexpected 
    behavior may occur, resulting in false positives in test results.

Libraries
---------

The framework uses Selenium WebDriver and python unittest libraries, documentation for which can be found below:

- `Selenium with Python <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`__
- `Python unit testing framework <https://docs.python.org/3/library/unittest.html>`__

Installation
============

After installing the above prerequisites, run:

::

    pip install webdriver-test-tools

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the
system

Command Line Usage
==================

For info on command line arguments:

::

    webdriver_test_tools --help

To initialize a new test project in the current directory:

::

    webdriver_test_tools --init

This will generate a new test package with template files and project
directories. For information and examples, see the `test project
documentation <http://connordelacruz.com/webdriver-test-tools/test_projects.html>`__.
