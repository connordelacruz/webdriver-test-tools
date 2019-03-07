
Installation
============

The ``webdriver_test_tools`` package utilizes Selenium WebDriver for automation,
which requires some additional set up on top of installing the package.


Prerequisites
-------------

Python
~~~~~~

The framework requires Python 3.4 or greater and ``pip``, which is included with
Python 3.4+ by default.

Drivers
~~~~~~~

In order to use Selenium, drivers will need to be installed for any browser
tests will be run on. The default browser configuration for test projects
enables Chrome and Firefox. To install these drivers using `Homebrew
<https://brew.sh/>`__ on macOS:

**Firefox:**

::

   brew install geckodriver

**Chrome:**

::

   brew cask install chromedriver

.. note::

   You may need to run ``brew tap homebrew/cask`` before attempting to install
   ``chromedriver``

For a list of all compatible drivers and an overview of what features are
supported by each, see :ref:`this table <driver-table>`.


Installing webdriver_test_tools
-------------------------------

After installing one or more compatible drivers, install
``webdriver_test_tools`` by running:

::

   pip install webdriver_test_tools

To verify the installation, check the version number by running:

::

   wtt --version

