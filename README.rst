====================
WebDriver Test Tools
====================

|pypi|
|github|

A front-end testing framework using `Selenium WebDriver`_ and Python.

.. |pypi| image:: https://img.shields.io/pypi/v/webdriver-test-tools.svg
    :alt: PyPI
    :target: http://pypi.python.org/pypi/webdriver-test-tools

.. |github| image:: https://img.shields.io/badge/GitHub--green.svg?style=social&logo=github
    :alt: GitHub
    :target: https://github.com/connordelacruz/webdriver-test-tools

.. _Selenium WebDriver: https://www.seleniumhq.org/docs/03_webdriver.jsp


.. contents::


Overview
========

WebDriver Test Tools provides a framework and utilities for writing front-end 
functional tests.


Features
--------

- Framework for writing cross-browser front-end test suites
- Pre-defined test functions for commonly used test procedures
- Utilities and extended functionality for the Selenium WebDriver package
- Implementation of the `Page Object Model`_ with pre-defined page objects for
  common elements (navbars, forms, etc)
- Command line tool for quickly generating files and directories for new test
  projects
- Mobile device layout emulation for responsive tests
- Headless browser testing
- Support for running tests on `BrowserStack`_

.. _Page Object Model: https://martinfowler.com/bliki/PageObject.html
.. _BrowserStack: https://www.browserstack.com/


This project uses Selenium WebDriver for automated browser actions and the
python unittest library for the test framework, documentation for which can be
found below:

- `Selenium with Python
  <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`__
- `Python unit testing framework
  <https://docs.python.org/3/library/unittest.html>`__


Documentation
-------------

Full documentation for WebDriver Test Tools:

    - `WebDriver Test Tools Docs`_: Framework documentation
    - `webdriver_test_tools Package API`_: Python package API

.. _WebDriver Test Tools Docs: http://connordelacruz.com/webdriver-test-tools/
.. _webdriver_test_tools Package API: http://connordelacruz.com/webdriver-test-tools/webdriver_test_tools.html


Set Up
======

Prerequisites
-------------

Python
~~~~~~

-  python 3+
-  pip

Drivers
~~~~~~~

In order to use Selenium, drivers will need to be installed for any browser
tests will be run on.

**Cross-Platform**

The following cross-platform browser drivers are supported and enabled by
default:

-  `Google Chrome`_
-  `Firefox`_

These can be disabled in ``<test_package>/config/browser.py`` by commenting out
the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``. 


**Platform-Specific**

The following platform-specific drivers are supported:

-  `Safari`_ 
-  `Internet Explorer`_
-  `Edge`_

These need to be enabled in ``<test_package>/config/browser.py`` by uncommenting
the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``.

.. _Google Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
.. _Firefox: https://github.com/mozilla/geckodriver/releases
.. _Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/ 
.. _Internet Explorer: https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver
.. _Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

The following documentation goes into detail on configuring browsers for
testing:

    - `Testing with Additional Browsers`_: Enabling/disabling browsers, per-test
      skipping for certain browsers, emulating mobile browsers, and headless
      browser testing
    - `BrowserStack Support`_: Enabling and configuring testing on BrowserStack

.. _Testing with Additional Browsers: http://connordelacruz.com/webdriver-test-tools/additional_browsers.html
.. _BrowserStack Support: http://connordelacruz.com/webdriver-test-tools/browserstack.html


Installation
------------

The package can be installed using pip:

.. code-block:: none

    pip install webdriver-test-tools

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the system.


Creating a Test Suite
---------------------

The package itself does not contain test cases. To generate files for a new test
suite, change into the desired directory and run:

.. code-block:: none

    webdriver_test_tools --init

This will generate a new test package with template files and project
directories.

The following documentation goes into detail on test projects:

    - `Test Project Overview`_: Test project setup, configuration, command line
      usage, and directory structure
    - `Example Test Project`_: Step-by-step tutorial with a simple example test
      project


.. _Test Project Overview: http://connordelacruz.com/webdriver-test-tools/test_projects.html
.. _Example Test Project: http://connordelacruz.com/webdriver-test-tools/example_project.html


Command Line Usage
==================

webdriver_test_tools
--------------------

For info on command line arguments:

.. code-block:: none

    webdriver_test_tools --help

To initialize a new test project in the current directory:

.. code-block:: none

    webdriver_test_tools --init

To print the version number:

.. code-block:: none

    webdriver_test_tools --version


.. readme-only
Test Projects
-------------

Test projects generated using ``webdriver_test_tools --init`` have their own 
set of command line arguments. For detailed information on test project command 
line usage and additional command line arguments, see the `Test Project 
Overview`_ documentation.

For info on command line arguments:

::

    python -m <test_package> --help

To print a list of available test classes and methods:

::

    python -m <test_package> --list

To run all tests:

::

    python -m <test_package>

To run all test cases in one or more modules:

::

    python -m <test_package> --module <test_module> [<test_module> ...]

To run specific TestCase classes:

::

    python -m <test_package> --test <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]

To do any of the above in specific browsers rather than running in all available
browsers:

::

    python -m <test_package> <args> --browser <browser> [<browser ...]

For a list of options you can specify with ``--browser``, run ``python -m
<test_package> --help``.

To improve performance, tests can be run in `headless browsers`_ using the
``--headless`` argument:

::

    python -m <test_package> <args> --headless

For a list of supported drivers, run ``python -m <test_package> --help``. For
details on using the ``--headless`` argument, see `Testing with Additional
Browsers`_.

.. _headless browsers: https://en.wikipedia.org/wiki/Headless_browser


Contributing
============

Please read the `contributing guidelines`_ for details.

.. _contributing guidelines: https://github.com/connordelacruz/webdriver-test-tools/blob/master/.github/CONTRIBUTING.rst



