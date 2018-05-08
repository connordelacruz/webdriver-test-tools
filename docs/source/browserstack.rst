BrowserStack Support
====================

.. contents::

Enabling BrowserStack support
-----------------------------

Testing with BrowserStack can be configured for a project in
``<test_package>/config/browserstack.py``. To enable BrowserStack support, set
``BrowserStackConfig.ENABLE`` to ``True`` and set
``BrowserStackConfig.USERNAME`` and ``BrowserStackConfig.ACCESS_KEY`` to your
BrowserStack account username and access key respectively. These values can be
found on the `BrowserStack Automate dashboard
<https://www.browserstack.com/automate>`__. 

.. code-block:: python
    :caption: config/browserstack.py

    class BrowserStackConfig(browserstack.BrowserStackConfig):
        ENABLE = True
        USERNAME = 'EXAMPLE'
        ACCESS_KEY = 'EXAMPLEKEY'


Running tests with BrowserStack
-------------------------------

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
--------------------

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


