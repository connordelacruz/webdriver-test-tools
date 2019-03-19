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
    :depth: 2


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
| `Google Chrome`_     | Yes                | Yes               | Yes           |
+----------------------+--------------------+-------------------+---------------+
| `Firefox`_           | Yes                | Yes               | No            |
+----------------------+--------------------+-------------------+---------------+
| `Safari`_            | No                 | No                | No            |
+----------------------+--------------------+-------------------+---------------+
| `Edge`_              | No                 | No                | No            |
+----------------------+--------------------+-------------------+---------------+
| `Internet Explorer`_ | No                 | No                | No            |
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

    wtt init

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

**Usage:**

::

    python -m <test_package> [-h] <command>

**Note:** If no ``<command>`` is specified, the ``run`` command will be
executed by default.


For info on command line arguments, use the ``--help`` (or ``-h``) argument:

::

    python -m <test_package> --help


Creating New Project Files
--------------------------

New tests and page objects can be generated using the ``new`` command:

::

    python -m <test_package> new [<type>] [<module_name>] [<ClassName>] [-d
    <description>] [-f]

Where:

- ``<type>``: The type of file to create (``test`` or ``page``)
- ``<module_name>``: Filename to use for the new python module
- ``<ClassName>``: Name to use for the initial class
- ``<description>``: (Optional) Description for the initial class
- ``-f``: (Optional) Force overwrite if a file with the same name already exists

If no arguments are provided, a prompt will walk you through generating the new
file. Alternatively, you can skip the prompts by using the arguments shown in
the following sections.


Creating New Tests
~~~~~~~~~~~~~~~~~~

New test modules can be generated using the ``new test`` command:

::

    python -m <test_package> new test <module_name> <TestCaseClass>

Where ``<module_name>`` is the filename for the new test and ``<TestCaseClass>``
is the class name for the test case.


The ``--description`` (or ``-d``) argument can be used to add a description for
the initial test case class:

::

    python -m <test_package> new test <module_name> <TestCaseClass> -d "Test case description"


If a test module with the same ``<module_name>`` already exists, ``new test``
will not overwrite it by default. The ``--force`` (or ``-f``) argument can be
used to force overwrite existing files:

::

    python -m <test_package> new test <module_name> <TestCaseClass> --force


Creating New Page Objects
~~~~~~~~~~~~~~~~~~~~~~~~~

New page object modules can be generated using the ``new page`` command:

::

    python -m <test_package> new page <module_name> <PageObjectClass>

Where ``<module_name>`` is the filename for the new module and
``<PageObjectClass>`` is the class name for the page object.


The ``--description`` (or ``-d``) argument can be used to add a description for
the initial page object class:

::

    python -m <test_package> new page <module_name> <PageObjectClass> -d "Page object description"


If a page module with the same ``<module_name>`` already exists, ``new page``
will not overwrite it by default. The ``--force`` (or ``-f``) argument can be
used to force overwrite existing files:

::

    python -m <test_package> new page <module_name> <PageObjectClass> --force


Running Tests
-------------

Basic Usage
~~~~~~~~~~~

To run all tests:

::

    python -m <test_package>


Running Specific Tests
~~~~~~~~~~~~~~~~~~~~~~

To run all test cases in one or more modules, use the ``--module`` (or ``-m``)
argument:

::

    python -m <test_package> --module <test_module> [<test_module> ...]

To run specific test case classes or methods, use the ``--test`` (or ``-t``)
argument:

::

    python -m <test_package> --test <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]

To skip certain test cases or methods, use the ``--skip`` (or ``-s``) argument:

::

    python -m <test_package> --skip <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]


The ``--test`` and ``--skip`` arguments both support wildcards (``*``) in class
and method names.

These arguments can be used together. When combined, they are processed in the
following order:

    1. ``--module`` reduces the set of tests to those in the specified modules
    2. ``--test`` reduces the set of tests to the specified classes and methods
    3. ``--skip`` removes the specified classes and methods from the set of tests


Using Specific Browsers
~~~~~~~~~~~~~~~~~~~~~~~

To do any of the above in specific browsers rather than running in all available
browsers, use the ``--browser`` (or ``-b``) argument:

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
``--headless`` (or ``-H``) argument:

::

    python -m <test_package> <args> --headless

**Note:** When using the ``--headless`` argument, tests will only be run with
the following web drivers that support running in a headless environment:

    * `Chrome <https://developers.google.com/web/updates/2017/04/headless-chrome>`__
    * `Firefox <https://developer.mozilla.org/en-US/Firefox/Headless_mode>`__

.. _headless browsers: https://en.wikipedia.org/wiki/Headless_browser


Using BrowserStack
~~~~~~~~~~~~~~~~~~

Test projects can be configured to run tests on `BrowserStack`_. Once
BrowserStack support is enabled, tests can be run on BrowserStack using the
``--browserstack`` (or ``-B``) argument:

::

    python -m <test_package> <args> --browserstack

See the documentation on `BrowserStack Support`_ for more details and setup
instructions.

.. _BrowserStack: https://www.browserstack.com/
.. _BrowserStack Support: https://connordelacruz.com/webdriver-test-tools/browserstack.html


Configuring Output
~~~~~~~~~~~~~~~~~~

By default, detailed output is displayed when running tests. To reduce or
suppress output, use the ``--verbosity`` (or ``-v``) argument:

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

    python -m <test_package> list

To only list test classes from specific modules:

::

    python -m <test_package> list --module <test_module> [<test_module> ...]

To only list specific test classes:

::

    python -m <test_package> list --test <TestClass> [<TestClass> ...]



Project Structure
=================

``wtt init`` will create the following files and directories
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
        ├── data.py
        ├── log/
        ├── pages/
        │   └── __init__.py
        ├── screenshot/
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
* ``data.py``: Module for storing static data for tests that must use specific
  values (e.g. emails, usernames, etc).


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

log/
~~~~

Default output directory for WebDriver logs. This can be changed in
``config/webdriver.py``.

pages/
~~~~~~

Page object classes for pages and components. These classes should handle
locating and interacting with elements on the page. See `Creating New Page
Objects`_ for info on generating new page object modules.

screenshot/
~~~~~~~~~~~

Default output directory for screenshots taken during test execution. This can 
be changed in ``config/webdriver.py``.

tests/
~~~~~~

Test case modules. These use page objects to interact with elements and assert
that the expected behavior occurs. See `Creating New Tests`_ for info on
generating new test modules.




