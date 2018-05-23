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

These can be disabled in ``<test_package>/config/browser.py`` by setting the
corresponding value in ``BrowserConfig.ENABLED_BROWSERS`` to ``False``. 


**Platform-Specific**

The following platform-specific drivers are supported:

-  `Safari`_ 
-  `Internet Explorer`_
-  `Edge`_

These need to be enabled in ``<test_package>/config/browser.py`` by setting the
corresponding value in ``BrowserConfig.ENABLED_BROWSERS`` to ``True``.

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

    webdriver_test_tools --init

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

For info on command line arguments:

::

    webdriver_test_tools --help

To initialize a new test project in the current directory:

::

    webdriver_test_tools --init

To print the version number:

::

    webdriver_test_tools --version


Contributing
============

Please read the `contributing guidelines`_ for details.

.. _contributing guidelines: https://github.com/connordelacruz/webdriver-test-tools/blob/master/.github/CONTRIBUTING.rst





=====================
Test Project Overview
=====================


Setup
=====

Initialization
--------------

To generate files for a new test suite, change into the desired directory and
run:

::

    webdriver_test_tools --init

This will generate a new test package with template files and project
directories.


Test Package Installation
-------------------------

After initializing the test project, run the following command from the project
root directory:

::

    pip install -e .

Installing with the ``-e`` flag will update the package automatically when
changes are made to the source code.

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the system


Configuration
-------------

After initializing a project, the URL of the site to be tested will need to be
configured. In ``<test_package>/config/site.py``, set the ``SITE_URL`` and
``BASE_URL`` of the ``SiteConfig`` class. You can add any other URLs you'll need
as class variables as well. 


Basic Command Line Usage
========================

For info on command line arguments:

::

    python -m <test_package> --help


Running Tests
-------------

To run all tests:

::

    python -m <test_package>

To run all test cases in one or more modules:

::

    python -m <test_package> --module <test_module> [<test_module> ...]

To run specific test case classes or methods:

::

    python -m <test_package> --test <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]

To skip certain test cases or methods:

::

    python -m <test_package> --skip <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]


These arguments can be used together. When combined, they are processed in the
following order:

    1. ``--module`` reduces the set of tests to those in the specified modules
    2. ``--test`` reduces the set of tests to the specified classes and methods
    3. ``--skip`` removes the specified classes and methods from the set of tests


Using Specific Browsers
~~~~~~~~~~~~~~~~~~~~~~~

To do any of the above in specific browsers rather than running in all available
browsers, use the ``--browser`` command line argument:

::

    python -m <test_package> <args> --browser <browser> [<browser ...]

For a list of options you can specify with ``--browser``, run ``python -m
<test_package> --help``.


Using Headless Browsers
~~~~~~~~~~~~~~~~~~~~~~~

By default, tests run using the browser's GUI. While it can be helpful to see
what's going on during test execution, loading and rendering the browser window
can be resource-intensive and slows down performance during test execution.

To improve performance, tests can be run in `headless browsers`_ using the
``--headless`` argument:

::

    python -m <test_package> <args> --headless

**Note:** When using the ``--headless`` argument, tests will only be run with
the following web drivers that support running in a headless environment:

    * `Chrome <https://developers.google.com/web/updates/2017/04/headless-chrome>`__
    * `Firefox <https://developer.mozilla.org/en-US/Firefox/Headless_mode>`__

.. _headless browsers: https://en.wikipedia.org/wiki/Headless_browser


Configuring Output
~~~~~~~~~~~~~~~~~~

By default, detailed output is displayed when running tests. To reduce or
suppress output:

::

    python -m <test_package> <args> --verbosity <level>

Where ``<level>`` is one of the following:

    * 0 - Final results only
    * 1 - Final results and progress indicator
    * 2 - Full output

**Note:** The default output level can be changed in
``<test_package>/config/test.py`` by setting the ``DEFAULT_VERBOSITY``
attribute of the ``TestSuiteConfig`` class.


List Available Tests
--------------------

To print a list of available test classes and methods:

::

    python -m <test_package> --list

To only list test classes from specific modules:

::

    python -m <test_package> --list --module <test_module> [<test_module> ...]

To only list specific test classes:

::

    python -m <test_package> --list --test <TestClass> [<TestClass> ...]



Project Structure
=================

``webdriver_test_tools --init`` will create the following files and directories
inside the project directory:

::

    <project-directory>/
    ├── README.rst
    ├── setup.py
    └── <test_package>/
        ├── __main__.py
        ├── __init__.py
        ├── config/
        │   ├── __init__.py
        │   ├── browser.py
        │   ├── browserstack.py
        │   ├── site.py
        │   ├── test.py
        │   └── webdriver.py
        ├── data/
        ├── log/
        ├── pages/
        ├── screenshot/
        ├── templates/
        │   ├── page_object.py
        │   └── test_case.py
        └── tests/
            └── __init__.py

This test structure is designed to be used with the `Page Object Model
<https://martinfowler.com/bliki/PageObject.html>`__. Interaction with the page
should be handled by page objects to minimize the need to alter tests whenever
the HTML is changed.


Test Project Root Contents
--------------------------

* ``setup.py``: Python package setup file that allows the new test suite to be
  installed as a pip package.


Test Package Root Contents
--------------------------

* ``__main__.py``: Required to run tests from the command line. 
* ``__init__.py``: Empty init file so Python recognizes the directory as a
  package.


Test Package Directories
------------------------

config/
~~~~~~~

Configurations used by test scripts for site URLs, web driver options, and the
python unittest framework.

* ``browser.py``: Configure which browsers to run tests in.
* ``browserstack.py``: Enable and configure testing with `BrowserStack
  <https://browserstack.com>`__.
* ``site.py``: Configure URLs used for testing.
* ``test.py``: Configure the ``unittest.TestRunner`` class.
* ``webdriver.py``: Configure WebDrivers and log output directory.


data/
~~~~~

Static data for tests that must use specific values (e.g. emails, usernames,
etc).

log/
~~~~

Default output directory for WebDriver logs. This can be changed in
``config/webdriver.py``.

pages/
~~~~~~

Page object classes for pages and components. These classes should handle
locating and interacting with elements on the page. A template page object can
be found in ``templates/page_object.py``.

screenshot/
~~~~~~~~~~~

Default output directory for screenshots taken during test execution. This can 
be changed in ``config/webdriver.py``.

tests/
~~~~~~

Test case modules. These use page objects to interact with elements and assert
that the expected behavior occurs. A template test file can be found in
``templates/test_case.py``.

When adding new test files, be sure to update ``tests/__init__.py`` to include
the new module so the framework can detect the new test cases.

templates/
~~~~~~~~~~

Template files to use as a starting point when writing new test modules or page
objects.

* ``page_object.py``: Template for page objects. Copy to the ``pages/``
  directory to use as a starting point when creating new page objects.
* ``test_case.py``: Template test module. Copy to the ``tests/`` directory to
  use as a starting point when creating new tests. 




