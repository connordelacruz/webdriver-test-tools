Test Project Overview
=====================

.. contents::

Basic Command Line Usage
------------------------

For info on command line arguments:

::

    python -m <test_package> --help

To run all tests:

::

    python -m <test_package>

To run all test cases in a file:

::

    python -m <test_package> --module <test_module>

Multiple modules can be run at once:

::

    python -m <test_package> --module <test_module0> <test_module1>

To run a single TestCase class in a file:

::

    python -m <test_package> --module <test_module> --test <TestClass>

To run just one test method in a TestCase class:

::

    python -m <test_package> --module <test_module> --test <TestClass>.<test_method>

The ``--module`` argument can be omitted when using the ``--test``
argument:

::

    python -m <test_package> --test <TestClass>

::

    python -m <test_package> --test <TestClass>.<test_method>

**Note:** This can be less efficient as each module will be searched for
the specified test, but the difference in performance will likely be
unnoticeable.

Multiple test classes and test methods can be run at once:

::
    
    python -m <test_package> --test <TestClass0> <TestClass1>.<test_method>

To do any of the above in a specific browser rather than running in all
available browsers, use the ``--browser <browser>`` command line
argument. For a list of options you can specify with ``--browser``, run
``python -m <test_package> --help``.

Project Structure
-----------------

``webdriver_test_tools --init`` will create the following files and
directories inside the project directory:

::

    <project-directory>/
    ├── README.md
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
        ├── templates/
        │   ├── page_object.py
        │   └── test_case.py
        └── tests/
            └── __init__.py

This test structure is best used with the `Page Object
Model <https://martinfowler.com/bliki/PageObject.html>`__. Interaction
with the page should be handled by page objects to minimize the need to
alter tests whenever the HTML is changed.

Test Project Root Contents
~~~~~~~~~~~~~~~~~~~~~~~~~~

``README.md`` is a template readme file with similar content to this
documentation. ``setup.py`` is a python package setup file that allows
the new test suite to be installed as a pip package.

Test Package Contents
~~~~~~~~~~~~~~~~~~~~~

config/
^^^^^^^

Configurations used by test scripts for site URLs, web driver options,
and the python unittest framework.

data/
^^^^^

Static data for tests that must use specific values (e.g. emails,
usernames, etc).

log/
^^^^

Default output directory for WebDriver logs.

pages/
^^^^^^

Page object classes for pages and components. These classes should
handle locating and interacting with elements on the page. A template
page object can be found in ``templates/page_object.py``.

tests/
^^^^^^

Test case modules. These use page objects to interact with elements and
assert that the expected behavior occurs. A template test file can be
found in ``templates/test_case.py``.

When adding new test files, be sure to update ``tests/__init__.py`` to
include the new module so the framework can detect the new test cases.

templates/
^^^^^^^^^^

Template files to use as a starting point when writing new test modules
or page objects.
