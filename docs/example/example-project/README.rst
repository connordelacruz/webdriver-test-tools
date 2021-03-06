====================
Example Test Project
====================

.. contents::

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
configured. In ``example_package/config/site.py``, set the ``SITE_URL`` and
``BASE_URL`` of the ``SiteConfig`` class. You can add any other URLs you'll need
as class variables as well. 


Basic Command Line Usage
========================

**Usage:**

::

    python -m example_package [-h] <command>

**Note:** If no ``<command>`` is specified, the ``run`` command will be
executed by default.


For info on command line arguments, use the ``--help`` (or ``-h``) argument:

::

    python -m example_package --help


Creating New Project Files
--------------------------

New tests and page objects can be generated using the ``new`` command:

::

    python -m example_package new [<type>] [<module_name>] [<ClassName>] [-d
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

    python -m example_package new test <module_name> <TestCaseClass>

Where ``<module_name>`` is the filename for the new test and ``<TestCaseClass>``
is the class name for the test case.


The ``--description`` (or ``-d``) argument can be used to add a description for
the initial test case class:

::

    python -m example_package new test <module_name> <TestCaseClass> -d "Test case description"


If a test module with the same ``<module_name>`` already exists, ``new test``
will not overwrite it by default. The ``--force`` (or ``-f``) argument can be
used to force overwrite existing files:

::

    python -m example_package new test <module_name> <TestCaseClass> --force


Creating New Page Objects
~~~~~~~~~~~~~~~~~~~~~~~~~

New page object modules can be generated using the ``new page`` command:

::

    python -m example_package new page <module_name> <PageObjectClass>

Where ``<module_name>`` is the filename for the new module and
``<PageObjectClass>`` is the class name for the page object.


The ``--description`` (or ``-d``) argument can be used to add a description for
the initial page object class:

::

    python -m example_package new page <module_name> <PageObjectClass> -d "Page object description"


If a page module with the same ``<module_name>`` already exists, ``new page``
will not overwrite it by default. The ``--force`` (or ``-f``) argument can be
used to force overwrite existing files:

::

    python -m example_package new page <module_name> <PageObjectClass> --force


Running Tests
-------------

Basic Usage
~~~~~~~~~~~

To run all tests:

::

    python -m example_package


Running Specific Tests
~~~~~~~~~~~~~~~~~~~~~~

To run all test cases in one or more modules, use the ``--module`` (or ``-m``)
argument:

::

    python -m example_package --module <test_module> [<test_module> ...]

To run specific test case classes or methods, use the ``--test`` (or ``-t``)
argument:

::

    python -m example_package --test <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]

To skip certain test cases or methods, use the ``--skip`` (or ``-s``) argument:

::

    python -m example_package --skip <TestClass>[.<test_method>] [<TestClass>[.<test_method>] ...]


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

    python -m example_package <args> --browser <browser> [<browser ...]

For a list of options you can specify with ``--browser``, run ``python -m
example_package --help``.


Using Headless Browsers
~~~~~~~~~~~~~~~~~~~~~~~

By default, tests run using the browser's GUI. While it can be helpful to see
what's going on during test execution, loading and rendering the browser window
can be resource-intensive and slows down performance during test execution.

To improve performance, tests can be run in `headless browsers`_ using the
``--headless`` (or ``-H``) argument:

::

    python -m example_package <args> --headless

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

    python -m example_package <args> --browserstack

See the documentation on `BrowserStack Support`_ for more details and setup
instructions.

.. _BrowserStack: https://www.browserstack.com/
.. _BrowserStack Support: https://connordelacruz.com/webdriver-test-tools/browserstack.html


Configuring Output
~~~~~~~~~~~~~~~~~~

By default, detailed output is displayed when running tests. To reduce or
suppress output, use the ``--verbosity`` (or ``-v``) argument:

::

    python -m example_package <args> --verbosity <level>

Where ``<level>`` is one of the following:

    * 0 - Final results only
    * 1 - Final results and progress indicator
    * 2 - Full output

**Note:** The default output level can be changed in
``example_package/config/test.py`` by setting the ``DEFAULT_VERBOSITY``
attribute of the ``TestSuiteConfig`` class.


List Available Tests
--------------------

To print a list of available test classes and methods:

::

    python -m example_package list

To only list test classes from specific modules:

::

    python -m example_package list --module <test_module> [<test_module> ...]

To only list specific test classes:

::

    python -m example_package list --test <TestClass> [<TestClass> ...]



Project Structure
=================

``wtt init`` will create the following files and directories
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


----

|webdriver_test_tools|

.. |webdriver_test_tools| image:: https://img.shields.io/badge/generated%20using-webdriver__test__tools%202.5.0-blue.svg?style=for-the-badge
    :alt: webdriver_test_tools 2.5.0


