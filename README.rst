Selenium WebDriver Test Tools
=============================

Utilities for writing front-end test suites using `Selenium WebDriver <https://www.seleniumhq.org/docs/03_webdriver.jsp>`__ and python unit tests.

.. contents::

Overview
--------

This project aims to reduce the amount of time and additional code
required to automate front-end functional testing by providing utilities
and conventions for building test suites.

This project uses Selenium WebDriver for automated browser actions and the python unittest library for the test framework. 

Prerequisites
-------------

python
~~~~~~

-  python 3+
-  pip

drivers
~~~~~~~

-  `geckodriver <https://github.com/mozilla/geckodriver/releases>`__
   (FireFox)
-  `chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__
   (Google Chrome)

On MacOS, both drivers can be installed using
`Homebrew <https://brew.sh/>`__:

::

    brew install geckodriver chromedriver

Support for more browser drivers will be added in future updates.

Libraries
~~~~~~~~~

The framework uses Selenium WebDriver and python unittest libraries, documentation for which can be found below:

- `Selenium with Python <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`__
- `Python unit testing framework <https://docs.python.org/3/library/unittest.html>`__

Installation
------------

After installing the above prerequisites, run:

::

    pip install webdriver-test-tools

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the
system

Command Line Usage
------------------

For info on command line arguments:

::

    webdriver_test_tools --help

To initialize a new test project in the current directory:

::

    webdriver_test_tools --init

This will generate a new test package with template files and project
directories. For information and examples, see the `test project
documentation <http://connordelacruz.com/webdriver-test-tools/test_projects.html>`__.
