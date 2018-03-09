Selenium WebDriver Test Framework
=================================

Utilities for writing front-end test suites using Selenium WebDriver and
python unit tests.

Overview
--------

This project aims to reduce the amount of time and additional code
required to automate front-end functional testing by providing utilities
and conventions for building test suites.

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

Installation
------------

After installing the above prerequisites, change to the root directory
of the project and run:

::

    pip install -e .

Installing with the ``-e`` flag will update the package automatically
when changes are made to the source code.

*Note:* Command may be ``pip3`` instead of ``pip`` depending on the
system

Command Line Usage
------------------

For info on command line arguments:

::

    python -m webdriver_test_tools --help

To initialize a new test project in the current directory:

::

    python -m webdriver_test_tools --init

This will generate a new test package with template files and project
directories.

*Note:* Command may be ``python3`` instead of ``python`` depending on
the system