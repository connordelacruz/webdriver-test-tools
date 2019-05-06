Example Project
===============

.. contents::

A quick example test project using ``webdriver_test_tools``. Source code for the
example project can be found `here
<https://github.com/connordelacruz/webdriver-test-tools/tree/master/docs/example/example-project>`__.


Initialize the project
----------------------

Create project files
~~~~~~~~~~~~~~~~~~~~

First, create a directory for the test project:

.. code-block:: none

    mkdir example-project
    cd example-project

Once in the project directory, run the following command to initialize the
project:

.. code-block:: none

    wtt init

You will be prompted to enter a name for the test project python package. To be
a valid package name, it needs to only use alphanumeric characters and
underscores and it cannot start with a number. For this example, we’ll call it
``example_package``:

.. code-block:: none
    :caption: Project creation prompt
    :emphasize-lines: 3,7,11,15

    Enter a name for the test package
    (use only alphanumeric characters and underscores. Cannot start with a number)
    > Package name: example_package
    
    (Optional) Enter a human-readable name for the test project
    (can use alphanumeric characters, spaces, hyphens, and underscores)
    > Project title [example_package]: Example Test Project
    
    Create .gitignore files for project root and log directory?
    (Ignores python cache files, package install files, local driver logs, etc)
    > Create .gitignore files (y/n) [y]:
    
    Generate README file?
    (README contains information on command line usage and directory structure)
    > Create README file (y/n) [y]:
    
    Creating test project...
    Project initialized.
    
    To get started, set the SITE_URL for the project in example_package/config/site.py 

    To create a new test, run:
       python -m example_package new test <module_name> <TestCaseClass>

    To create a new page object, run:
       python -m example_package new page <module_name> <PageObjectClass>

    For more information, visit <https://connordelacruz.com/webdriver-test-tools/>

Initializing the project should create the following files and directories:

.. code-block:: none
    :caption: Example project file structure

    example-project/
    ├── README.rst
    ├── example_package/
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── config/
    │   │   ├── __init__.py
    │   │   ├── browser.py
    │   │   ├── browserstack.py
    │   │   ├── projectfiles.py
    │   │   ├── site.py
    │   │   ├── test.py
    │   │   └── webdriver.py
    │   ├── data.py
    │   ├── log/
    │   ├── pages/
    │   │   └── __init__.py
    │   ├── screenshot/
    │   └── tests/
    │       └── __init__.py
    └── setup.py


(Optional) Setup virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If using ``virtualenv``, initialize the virtual environment before installing
the test package:

.. code-block:: none
   
   virtualenv venv
   source ./venv/bin/activate

``virtualenv`` allows the test package to be installed in an isolated python
environment, ensuring any dependencies won't overlap with other packages that
may require different versions. For more information, see `virtualenv
documentation <https://virtualenv.pypa.io/en/latest/>`_.


Install test package
~~~~~~~~~~~~~~~~~~~~

After initializing the test project, run:

.. code-block:: none

    pip install -e .

Installing with the ``-e`` flag will update the package automatically when
changes are made to the source code.

.. note::

   If you don't want to install test project packages, you can still run them
   from the project root directory using ``python -m <test_package>``.


Configure site URLs
-------------------

After initializing a project, the URL of the site to be tested will need to be
configured. In ``example_package/config/site.py``, set the ``SITE_URL`` and
``BASE_URL`` of the ``SiteConfig`` class.

For this example, we’ll use `example.com <https://www.example.com/>`__.

.. literalinclude:: ../example/example-project/example_package/config/site.py
    :caption: config/site.py:
    :lines: 1-12
    :emphasize-lines: 7,9


We’ll be testing that clicking a link takes us to an external page, so we’ll add
another variable ``INFO_URL`` to ``SiteConfig``:

.. literalinclude:: ../example/example-project/example_package/config/site.py
    :caption: config/site.py:
    :lines: 1-
    :emphasize-lines: 13-14


Add a page object
-----------------

Creating a new page object module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This test framework is best used with the `Page Object Model
<https://martinfowler.com/bliki/PageObject.html>`__. Interaction with the page
should be handled by page objects to minimize the need to alter tests whenever
the HTML is changed.

After configuring URLs, we’ll want to add a page object for the home
page of example.com. Run the following command to create a new page object
module:

.. code-block:: none

    example_package new page

You will be prompted to enter a name for the new module, a class name for the
new page object, and an optional description for the page object. We'll call the
new page module ``home`` and the new page object class ``HomePage``:

.. code-block:: none
   :caption: New page object prompt
   :emphasize-lines: 2,5,8,16

   Enter a file name for the new page module
   > Module file name: home
   
   Enter a name for the initial page object class
   > Page object class name: HomePage
   
   (Optional) Enter description of the new page object class
   > Description []:

   (Optional) Select a page object prototype to subclass:
      [1] form
      [2] modal
      [3] nav
      [4] collapsible nav
      [5] web page
   > Page object prototype []:

This will create the file ``example_package/pages/home.py``.

.. note::

   For more information on the ``new page`` command, run:

   ::

      example_package new page --help


Locating page elements
~~~~~~~~~~~~~~~~~~~~~~

For any element we need to locate, we’ll want to keep track of how to target it
in the ``Locator`` subclass. Selenium WebDriver locators are tuples in the
format ``(By.<selection type>, <selection string>)``, where ``<selection type>``
is one of the constants declared in ``selenium.webdriver.common.by.By`` and
``<selection string>`` is the string used to find the element.

Example.com is a pretty bare bones website, so these examples will be pretty
contrived. We’ll add locators for the site heading and the ‘More information…’
link.

To locate the ‘More information…’ link, we’re going to select it by its link
text. Add ``HEADING`` and ``INFO_LINK`` variables to the ``Locator`` subclass:

.. literalinclude:: ../example/example-project/example_package/pages/home.py
    :caption: pages/home.py:
    :lines: 6-13
    :emphasize-lines: 7-8


.. note::

   The utility function ``locate.by_element_text()`` returns an XPATH locator
   for elements with the specified text.


Interacting with page elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For our example tests, we’ll want to look at the heading text and click on the
‘More information…’ link. Add the following functions to the ``HomePage`` class:

.. literalinclude:: ../example/example-project/example_package/pages/home.py
    :caption: pages/home.py:
    :pyobject: HomePage
    :emphasize-lines: 10-12,14-16

.. note::

   The ``BasePage`` method ``self.find_element(locator)`` is shorthand for
   ``self.driver.find_element(*locator)``. 


Add a test
----------

Creating a new test module
~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that we have a page object for interacting with example.com, we can write a
test case. Run the following command to create a new test module:

.. code-block:: none

    example_package new test

You will be prompted to enter a name for the new module, a class name for the
test case, and an optional description for the test case class. We'll call the
new test module ``home`` and the new test case class ``HomePageTestCase`` with
the description **"Really contrived example test case"**:

.. code-block:: none
   :caption: New test prompt
   :emphasize-lines: 2,5,8

   Enter a file name for the new test module
   > Module file name: home
   
   Enter a name for the initial test case class
   > Test case class name: HomePageTestCase
   
   (Optional) Enter description of the new test case class
   > Description []: Really contrived example test case

This will create the file ``example_package/tests/home.py``.

.. note::

   For more information on the ``new test`` command, run:

   ::

      example_package new test --help


Adding test functions
~~~~~~~~~~~~~~~~~~~~~

So far we have created a page object for the home page and an empty test case
for home page tests. Now we're going to add some test functions to
``HomePageTestCase``.

In ``tests/home.py``, import the ``HomePage`` class we created:

.. literalinclude:: ../example/example-project/example_package/tests/home.py
    :caption: tests/home.py:
    :lines: 1-10
    :emphasize-lines: 6

We’re going to add 2 test functions:

1. Retrieve the heading text and assert that it says ‘Example Domain’
2. Click the ‘More information…’ link and assert that the URL matches
   ``SiteConfig.INFO_URL``

.. literalinclude:: ../example/example-project/example_package/tests/home.py
    :caption: tests/home.py:
    :lines: 9-
    :emphasize-lines: 9-13,15-20


.. note::

    Test functions need to begin with the prefix ``test_`` in order for
    the python ``unittest`` library to recognize them as tests.

The method ``WebDriverTestCase.assertUrlChange()`` tests that the current URL
matches the URL given as a parameter, (waiting a few seconds for the page to
load before reporting a failure). The ``WebDriverTestCase`` class includes a
number of additional assertion methods for WebDriver testing. For more
information, see the :ref:`list of WebDriverTestCase assertion methods
<assertion-methods>`.

We should now have everything we need to run our test suite. To verify that the
framework is able to detect the tests, run:

.. code-block:: none

    example_package list

This prints a list of test cases and their test methods in the package. The
output should look like this:

.. code-block:: none

   home:
      HomePageTestCase:
         test_more_information_link
         test_page_heading

You can also run ``example_package list --verbose`` to view the docstring for
each class and method:

.. code-block:: none

   home:
   └── HomePageTestCase:
       Really contrived example test case
       ├── test_more_information_link
       │   Test that the 'More information...' link goes to the correct URL
       └── test_page_heading
           Ensure that the page heading text is correct


Run the tests
-------------

.. image:: ./_static/example_package.gif


Running the test suite
~~~~~~~~~~~~~~~~~~~~~~

To run our test suite:

.. code-block:: none

    example_package

This will generate new test case classes for Chrome and Firefox based on the
test case classes we wrote and run them. If all tests pass, the output should
look like this:

.. code-block:: none

    (Firefox) Really contrived example test case
        Test that the 'More information...' link goes to the correct URL ... ok
        Ensure that the page heading text is correct ... ok
    (Chrome) Really contrived example test case
        Test that the 'More information...' link goes to the correct URL ... ok
        Ensure that the page heading text is correct ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 15.436s

    OK


Optional command line arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test packages can be run with various optional arguments to run a limited set of
test cases instead of running the entire suite. To see a list of command line
arguments, run:

.. code-block:: none

    example_package run --help

Running in a specific browser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we just wanted to run the tests in a specific browser, we can use the
``--browser`` command line argument. For example, if we only wanted to run
Firefox test cases:

.. code-block:: none

    example_package --browser firefox

Running specific test modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we only want to run a specific test module, we can use the ``--module``
command line argument. For example, if we just wanted to run
``tests/home.py``:

.. code-block:: none

    example_package --module home

Since we only have one test module in this example, this doesn’t do anything
different than normal, but this can be useful in test projects with multiple
test modules.

Running specific test cases or functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we only want to run a specific test case or function within a test case, we
can use the ``--test`` command line argument. For example, if we just wanted to
run HomePageTestCase:

.. code-block:: none

    example_package --test HomePageTestCase

Since we only have one test case class in this example, this doesn’t do anything
different than normal, but this can be useful in test projects with multiple
cases.

If we just wanted to run the ``test_more_information_link`` function:

.. code-block:: none

    example_package --test HomePageTestCase.test_more_information_link

The ``--test`` argument also supports wildcards in both the test case class and
method names. For example, if we wanted to run all test case classes beginning
with the word ``Home``:

.. code-block:: none

   example_package --test Home*

Or if we wanted to run all methods in ``HomePageTestCase`` containing the word
``page``:

.. code-block:: none

   example_package --test HomePageTestCase.*page*

Or if we wanted to run all test methods ending with the word ``link``:

.. code-block:: none

   example_package --test *.*_link

Obviously this isn't particularly useful in our simple example, but can allow
for a lot more control in larger test projects without needing to type out long
lists of test cases and methods.

Skipping test cases or functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we wanted to skip a test case or function within a test case, we can use the
``--skip`` command line argument, which uses the same syntax as ``--test``. For 
example, if we wanted to run all tests except for the
``test_more_information_link`` function:

.. code-block:: none

    example_package --skip HomePageTestCase.test_more_information_link

Like the ``--test`` argument, ``--skip`` also supports wildcards in class and
method names. E.g. if we wanted to skip all methods in all test cases that
contain the word ``page``:

.. code-block:: none

    example_package --skip *.*page*

Again, this isn't particularly interesting since we only have 2 test functions,
but can be useful in larger test projects.

Running tests in headless browsers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some browsers support headless execution. This allows tests to be run without 
the browser GUI, which improves performance. To run the example test suite in
headless browsers:

.. code-block:: none

    example_package --headless

For more information and a list of compatible browsers, see 
:ref:`headless browsers documentation <headless-browsers>`. 

Running tests silently
^^^^^^^^^^^^^^^^^^^^^^

By default, detailed output is displayed when running tests. If we wanted to
reduce the output to just a progress bar and the final results while running
tests:

.. code-block:: none

    example_package --verbosity 1

To suppress output entirely and just get the final results:

.. code-block:: none

    example_package --verbosity 0



