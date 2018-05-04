Example Test Project
====================

.. contents::

Setup
-----

Installation
~~~~~~~~~~~~

After initializing the test project, change to the root directory of the project
and run:

::

    pip install -e .

Installing with the ``-e`` flag will update the package automatically when
changes are made to the source code.

**Note:** Command may be ``pip3`` instead of ``pip`` depending on the system


Configuration
~~~~~~~~~~~~~

After initializing a project, the URL of the site to be tested will need to be
configured. In ``example_package/config/site.py``, set the ``SITE_URL`` and
``BASE_URL`` of the ``SiteConfig`` class. You can add any other URLs you'll need
as class variables as well. 


Basic Command Line Usage
------------------------

For info on command line arguments:

::

    python -m example_package --help


Running Tests
~~~~~~~~~~~~~

To run all tests:

::

    python -m example_package

To run all test cases in one or more modules:

::

    python -m example_package --module <test_module> [<test_module> ...]

To run specific TestCase classes:

::

    python -m example_package --test <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]

The ``--test`` argument will run all tests in a class if no method is specified
for it.

**Note:** If the ``--module`` and ``--test`` arguments are used together, only
the specified modules will be searched when looking for the specified test
classes. If any of the test classes do not exist in any of the specified
modules, they will be ignored.


Using Specific Browsers
^^^^^^^^^^^^^^^^^^^^^^^

To do any of the above in specific browsers rather than running in all available
browsers, use the ``--browser`` command line argument:

::

    python -m example_package <args> --browser <browser> [<browser ...]

For a list of options you can specify with ``--browser``, run ``python -m
example_package --help``.


Using Headless Browsers
^^^^^^^^^^^^^^^^^^^^^^^

By default, tests run using the browser's GUI. While it can be helpful to see
what's going on during test execution, loading and rendering the browser window
can be resource-intensive and slows down performance during test execution.

To improve performance, tests can be run in `headless browsers`_ using the
``--headless`` argument:

::

    python -m example_package <args> --headless

**Note:** When using the ``--headless`` argument, tests will only be run with
the following web drivers that support running in a headless environment:

    * `Chrome <https://developers.google.com/web/updates/2017/04/headless-chrome>`__
    * `Firefox <https://developer.mozilla.org/en-US/Firefox/Headless_mode>`__

.. _headless browsers: https://en.wikipedia.org/wiki/Headless_browser


List Available Tests
~~~~~~~~~~~~~~~~~~~~

To print a list of available test classes and methods:

::

    python -m example_package --list

To only list test classes from specific modules:

::

    python -m example_package --list --module <test_module> [<test_module> ...]

To only list specific test classes:

::

    python -m example_package --list --test <TestClass> [<TestClass> ...]


Project Structure
-----------------

``webdriver_test_tools --init`` will create the following files and directories
inside the project directory:

::

    <project-directory>/
    ├── README.rst
    ├── setup.py
    └── example_package/
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
~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``setup.py``: Python package setup file that allows the new test suite to be
  installed as a pip package.


Test Package Root Contents
~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``__main__.py``: Required to run tests from the command line. 
* ``__init__.py``: Empty init file so Python recognizes the directory as a
  package.


Test Package Directories
~~~~~~~~~~~~~~~~~~~~~~~~

config/
^^^^^^^

Configurations used by test scripts for site URLs, web driver options, and the
python unittest framework.

* ``browser.py``: Configure which browsers to run tests in.
* ``browserstack.py``: Enable and configure testing with `BrowserStack
  <https://browserstack.com>`__.
* ``site.py``: Configure URLs used for testing.
* ``test.py``: Configure the ``unittest.TestRunner`` class.
* ``webdriver.py``: Configure WebDrivers and log output directory.


data/
^^^^^

Static data for tests that must use specific values (e.g. emails, usernames,
etc).

log/
^^^^

Default output directory for WebDriver logs. This can be changed in
``config/webdriver.py``.

pages/
^^^^^^

Page object classes for pages and components. These classes should handle
locating and interacting with elements on the page. A template page object can
be found in ``templates/page_object.py``.

tests/
^^^^^^

Test case modules. These use page objects to interact with elements and assert
that the expected behavior occurs. A template test file can be found in
``templates/test_case.py``.

When adding new test files, be sure to update ``tests/__init__.py`` to include
the new module so the framework can detect the new test cases.

templates/
^^^^^^^^^^

Template files to use as a starting point when writing new test modules or page
objects.

* ``page_object.py``: Template for page objects. Copy to the ``pages/``
  directory to use as a starting point when creating new page objects.
* ``test_case.py``: Template test module. Copy to the ``tests/`` directory to
  use as a starting point when creating new tests. 


----

|webdriver_test_tools|

.. |webdriver_test_tools| image:: https://img.shields.io/badge/generated%20using-webdriver__test__tools%200.27.0-blue.svg?style=for-the-badge
    :alt: webdriver_test_tools 0.27.0

