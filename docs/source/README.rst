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

.. _WebDriver Test Tools Docs: https://connordelacruz.com/webdriver-test-tools/
.. _webdriver_test_tools Package API: https://connordelacruz.com/webdriver-test-tools/webdriver_test_tools.html


Set Up
======

Prerequisites
-------------

Python
~~~~~~

-  Python 3.4+
-  pip (included by default with Python 3.4+)

Drivers
~~~~~~~

.. _driver-table:

In order to use Selenium, drivers will need to be installed for any browser
tests will be run on. Below are currently supported drivers, their default
enabled/disabled status, and their supported features:

+----------------------+--------------------+-------------------+---------------+
| Driver               | Enabled by Default | Headless Browsing | Mobile Layout |
+======================+====================+===================+===============+
| `Google Chrome`_     | ✓                  | ✓                 | ✓             |
+----------------------+--------------------+-------------------+---------------+
| `Firefox`_           | ✓                  | ✓                 |               |
+----------------------+--------------------+-------------------+---------------+
| `Safari`_            |                    |                   |               |
+----------------------+--------------------+-------------------+---------------+
| `Edge`_              |                    |                   |               |
+----------------------+--------------------+-------------------+---------------+
| `Internet Explorer`_ |                    |                   |               |
+----------------------+--------------------+-------------------+---------------+

Cross-platform browsers are enabled by default, while platform-specific browsers
are disabled by default. You can enable or disable drivers in
``<test_package>/config/browser.py`` by setting the corresponding value in
``BrowserConfig.ENABLED_BROWSERS`` to ``True`` or ``False``, respectively.

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

.. _Testing with Additional Browsers: https://connordelacruz.com/webdriver-test-tools/additional_browsers.html
.. _BrowserStack Support: https://connordelacruz.com/webdriver-test-tools/browserstack.html


Installation
------------

The package can be installed using pip:

::

    pip install webdriver-test-tools

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the system.


Creating a Test Suite
---------------------

The package itself does not contain test cases. To generate files for a new test
suite, change into the desired directory and run:

::

    wtt init

This will generate a new test package with template files and project
directories.

The following documentation goes into detail on test projects:

    - `Test Projects`_: Test project setup, configuration, command line usage,
      and directory structure
    - `Example Test Project`_: Step-by-step tutorial with a simple example test
      project


.. _Test Projects: https://connordelacruz.com/webdriver-test-tools/test_projects.html
.. _Example Test Project: https://connordelacruz.com/webdriver-test-tools/example_project.html


Command Line Usage
==================

To initialize a new test project in the current directory:

::

    wtt init [<package_name>] [<"Project Title">] [--no-gitignore] [--no-readme]

Where:

- ``<package_name>``: Name for the new test package. (alphanumeric characters
  and underscores only. Cannot start with a number)
- ``<"Project Title">``: (Optional) Friendly name for the test project. Defaults
  to the value of <package_name> if not provided
- ``--no-gitignore``: Do not create .gitignore files for project root and log
  directory
- ``--no-readme``: Do not generate README file with usage info

If no arguments are provided, a prompt will walk you through project
initialization.

For info on command line arguments:

::

    wtt --help

To print the version number:

::

    wtt --version

**Note:** ``wtt`` and ``webdriver_test_tools`` can be used interchangeably.


Contributing
============

Please read the `contributing guidelines`_ for details on reporting bugs,
requesting features, and making contributions to the project.

.. _contributing guidelines: https://github.com/connordelacruz/webdriver-test-tools/blob/master/.github/CONTRIBUTING.rst



