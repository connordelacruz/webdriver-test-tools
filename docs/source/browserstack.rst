====================
BrowserStack Support
====================

.. contents::

Enabling BrowserStack support
=============================

Testing with BrowserStack can be configured for a project in
``<test_package>/config/browserstack.py``. To enable BrowserStack support, set
``BrowserStackConfig.ENABLE`` to ``True`` and set
``BrowserStackConfig.USERNAME`` and ``BrowserStackConfig.ACCESS_KEY`` to your
BrowserStack account username and access key respectively. These values can be
found on the `BrowserStack Automate dashboard
<https://automate.browserstack.com>`__. 

.. code-block:: python
    :caption: config/browserstack.py

    class BrowserStackConfig(browserstack.BrowserStackConfig):
        ENABLE = True
        USERNAME = 'EXAMPLE'
        ACCESS_KEY = 'EXAMPLEKEY'


Running tests with BrowserStack
===============================

After enabling and configuring BrowserStack, use the ``--browserstack`` command
line argument to run tests on BrowserStack instead of running locally. Some
examples:

::

    python -m <test_package> --browserstack

::

    python -m <test_package> --module <test_module> --browserstack

::

    python -m <test_package> --test <TestClass> --browserstack

::

    python -m <test_package> --browser <browser> --browserstack


Configuring Browsers
====================

By default, BrowserStack tests are generated for Firefox and Chrome. Additional 
browsers can be enabled in ``<test_package>/config/browserstack.py``. For 
example, to enable test cases for Internet Explorer, set ``Browsers.IE`` to
``True`` in ``BrowserStackConfig.ENABLED_BROWSERS``:


.. code-block:: python
    :caption: config/browserstack.py
    :emphasize-lines: 7

    class BrowserStackConfig(browserstack.BrowserStackConfig):
        ...
        ENABLED_BROWSERS = {
            Browsers.FIREFOX: True,
            Browsers.CHROME: True,
            Browsers.SAFARI: False,
            Browsers.IE: True,
            Browsers.EDGE: False,
            Browsers.CHROME_MOBILE: False,
        }


Additional Configurations
=========================

BrowserStack tests support additional configurations using the 
``BrowserStackConfig.BS_CAPABILITIES`` dictionary. For a list of BrowserStack's 
configurable capabilities, see their `capabilities documentation 
<https://www.browserstack.com/automate/capabilities>`__.


Rename the Project
------------------

By default, the project name is set to the test package name. This can be
reconfigured by setting ``'project'`` to the desired name in ``BrowserStackConfig.BS_CAPABILITIES``:

.. code-block:: python
    :caption: config/browserstack.py
    :emphasize-lines: 3

    BS_CAPABILITIES = {
        ...
        'project': 'Custom Name',
        ...
    }


Specifying the Build Name
-------------------------

BrowserStack supports grouping related project tests under a build name. To
specify the build name for the group of tests being run:

::

    python -m <test_package> <args> --browserstack --build <name>

**Note:** Quotation marks must be used for build names containing spaces (e.g.
``--build 'Example Build'``).


Enabling Video
--------------

Video recording can be enabled for tests run on BrowserStack by setting
``'browserstack.video'`` to ``True`` in ``BrowserStackConfig.BS_CAPABILITIES``:

.. code-block:: python
    :caption: config/browserstack.py
    :emphasize-lines: 3

    BS_CAPABILITIES = {
        ...
        'browserstack.video': True,
        ...
    }

This config option is set to ``False`` by default as it slows down test 
execution, but it can be useful to see what's happening while testing.

To view the recorded videos, go to https://automate.browserstack.com and
select the test on the left column.

Command Line Arguments
~~~~~~~~~~~~~~~~~~~~~~

The video configuration can be overridden by using the ``--video`` or
``--no-video`` arguments.

To enable video recording:

::

    python -m <test_package> <args> --browserstack --video

To disable video recording:

::

    python -m <test_package> <args> --browserstack --no-video



