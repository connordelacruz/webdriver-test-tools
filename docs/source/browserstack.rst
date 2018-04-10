BrowserStack Support
====================

.. contents::

Enabling BrowserStack support
-----------------------------

Testing with BrowserStack can be configured for a project in ``<test_package>/config/browserstack.py``. To enable BrowserStack support, set ``BrowserStackConfig.ENABLE`` to ``True`` and set ``BrowserStackConfig.USERNAME`` and ``BrowserStackConfig.ACCESS_KEY`` to your BrowserStack account username and access key respectively. These values can be found on the `BrowserStack Automate dashboard <https://www.browserstack.com/automate>`__. 

``config/browserstack.py``:

.. code:: python

    class BrowserStackConfig(browserstack.BrowserStackConfig):
        ENABLE = True
        USERNAME = 'EXAMPLE'
        ACCESS_KEY = 'EXAMPLEKEY'


Running tests with BrowserStack
-------------------------------

After enabling and configuring BrowserStack, use the ``--browserstack`` command line argument to run tests on BrowserStack instead of running locally. Some examples:

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

By default, BrowserStack tests are generated for the same browsers enabled in ``<test_package>/config/browser.py``. To enable additional browsers when testing with BrowserStack, modify ``BrowserStackConfig._additional_browsers``. For example, to enable test cases for Internet Explorer, uncomment the corresponding line in the config file:

``config/browserstack.py``:

.. code:: python

    class BrowserStackConfig(browserstack.BrowserStackConfig):
        ...
        # Defaults to using the same browsers configured in BrowserConfig class
        BROWSER_TEST_CLASSES = BrowserConfig.BROWSER_TEST_CLASSES.copy()
        # Add additional browsers here:
        _additional_browsers = {
            # Browsers.FIREFOX: FirefoxTestCase,
            # Browsers.CHROME: ChromeTestCase,
            # Browsers.SAFARI: SafariTestCase,
            Browsers.IE: IETestCase,
            # Browsers.EDGE: EdgeTestCase,
            # Browsers.CHROME_MOBILE: ChromeMobileTestCase,
        }
        BROWSER_TEST_CLASSES.update(_additional_browsers)


BrowserStack browsers can be configured independently of ``BrowserConfig`` by setting ``BrowserStackConfig.BROWSER_TEST_CLASSES`` directly instead of copying the configurations from ``BrowserConfig``. For example, if you only wanted to enable Internet Explorer for BrowserStack tests:

``config/browserstack.py``:

.. code:: python

    class BrowserStackConfig(browserstack.BrowserStackConfig):
        ...
        BROWSER_TEST_CLASSES = {
            # Browsers.FIREFOX: FirefoxTestCase,
            # Browsers.CHROME: ChromeTestCase,
            # Browsers.SAFARI: SafariTestCase,
            Browsers.IE: IETestCase,
            # Browsers.EDGE: EdgeTestCase,
            # Browsers.CHROME_MOBILE: ChromeMobileTestCase,
        }


