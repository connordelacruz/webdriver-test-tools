=============================
Selenium WebDriver Test Tools
=============================

|pypi|
|github|

.. |pypi| image:: https://img.shields.io/pypi/v/webdriver-test-tools.svg
    :alt: PyPI
    :target: http://pypi.python.org/pypi/webdriver-test-tools

.. |github| image:: https://img.shields.io/badge/GitHub--green.svg?style=social&logo=github
    :alt: GitHub
    :target: https://github.com/connordelacruz/webdriver-test-tools


Utilities for writing front-end test suites using `Selenium WebDriver <https://www.seleniumhq.org/docs/03_webdriver.jsp>`__ and python unit tests.


.. contents::


Overview
========

This project aims to reduce the amount of time and additional code required to automate front-end functional testing by providing utilities and conventions for building test suites. 


Features
--------

- Utilities and extended functionality for the Selenium WebDriver package
- Pre-defined test methods for commonly used test procedures
- Unit testing framework for automated tests on multiple browsers
- Implementation of the `Page Object Model <https://martinfowler.com/bliki/PageObject.html>`__ and pre-defined page objects for common elements (navbars, forms, etc)
- Command line tool for quickly generating files and directories for new test projects
- Support for automating tests on `BrowserStack <https://www.browserstack.com/>`__


This project uses Selenium WebDriver for automated browser actions and the python unittest library for the test framework, documentation for which can be found below:

- `Selenium with Python <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`__
- `Python unit testing framework <https://docs.python.org/3/library/unittest.html>`__


Creating a Test Suite
---------------------

The package itself does not contain test cases. To generate files for a new test suite, change into the desired directory and run:

::

    webdriver_test_tools --init

This will generate a new test package with template files and project directories. 

For information on the test package structure and command line arguments, see the `test project documentation <http://connordelacruz.com/webdriver-test-tools/test_projects.html>`__.

For information on setting up a test project and writing tests using the ``webdriver_test_tools`` framework, see the `example test project documentation <http://connordelacruz.com/webdriver-test-tools/example_project.html>`__.


Prerequisites
=============

Python
------

-  python 3+
-  pip

Drivers
-------

In order to use Selenium, drivers will need to be installed for any browser tests will be run on.

Cross-Platform
~~~~~~~~~~~~~~

The following cross-platform browser drivers are supported and enabled by default:

-  `geckodriver <https://github.com/mozilla/geckodriver/releases>`__
   (FireFox)
-  `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__
   (Google Chrome)

These can be disabled in ``<test_package>/config/browser.py`` by commenting out the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``. 


Platform-Specific
~~~~~~~~~~~~~~~~~

The following platform-specific drivers are supported:

-  `Safari <https://webkit.org/blog/6900/webdriver-support-in-safari-10/>`__ 
-  `Internet Explorer <https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver>`__
-  `Edge <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`__

These need to be enabled in ``<test_package>/config/browser.py`` by uncommenting the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``.

For information on usage and considerations, see the `additional browsers documentation <http://connordelacruz.com/webdriver-test-tools/additional_browsers.html>`__.


Installation
============

The package can be installed using pip:

::

    pip install webdriver-test-tools

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the system.


Command Line Usage
==================

For info on command line arguments:

::

    webdriver_test_tools --help

To initialize a new test project in the current directory:

::

    webdriver_test_tools --init

