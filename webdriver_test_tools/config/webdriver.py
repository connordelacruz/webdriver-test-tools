import os
from datetime import datetime

from selenium import webdriver

import webdriver_test_tools
from webdriver_test_tools.common import utils


class WebDriverConfig:
    """Configurations for webdriver

    :var WebDriverConfig.LOG_PATH: Path to the log directory. Defaults to the log
        subdirectory in the webdriver_test_tools package root directory
    :var WebDriverConfig.SCREENSHOT_PATH: Path to the screenshot directory. Defaults
        to the screenshot subdirectory in the webdriver_test_tools package root directory
    :var WebDriverConfig.IMPLICIT_WAIT: Implicit wait time for webdriver to poll DOM

        .. note::

            Documentation says not to mix this with explicit waits and some instability
            was noticed when it was set to 10. Projects can override this if necessary.
            `Implicit wait documentation
            <https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#explicit-and-implicit-waits>`__

    Browser driver initialization arguments:

    :var WebDriverConfig.FIREFOX_KWARGS: Keyword args for ``webdriver.Firefox()``
    :var WebDriverConfig.CHROME_KWARGS: Keyword args for ``webdriver.Chrome()``
    :var WebDriverConfig.SAFARI_KWARGS: Keyword args for ``webdriver.Safari()``
    :var WebDriverConfig.IE_KWARGS: Keyword args for ``webdriver.Ie()``
    :var WebDriverConfig.EDGE_KWARGS: Keyword args for ``webdriver.Edge()``

    .. note::

        Logging configurations are set when the corresponding ``get_<browser>_driver()``
        method is called. This allows for projects to override the ``LOG_PATH`` variable
        without having to also override all ``<browser>_KWARGS`` variables as well.

    Mobile configurations:

    :var WebDriverConfig.CHROME_MOBILE_EMULATION: Dictionary with 'mobileEmulation'
        options for Chrome

    Headless browser configurations:

    :var WebDriverConfig.CHROME_HEADLESS_ARGS: Command line arguments to use in addition
        to the ``--headless`` flag
    :var WebDriverConfig.FIREFOX_HEADLESS_ARGS: Command line arguments to use in addition
        to the ``-headless`` flag
    """
    # Root directory of webdriver_test_tools package
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(webdriver_test_tools.__file__))
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')
    SCREENSHOT_PATH = os.path.join(_PACKAGE_ROOT, 'screenshot')

    IMPLICIT_WAIT = 0

    FIREFOX_KWARGS = {}
    CHROME_KWARGS = {}
    SAFARI_KWARGS = {}
    IE_KWARGS = {}
    EDGE_KWARGS = {}

    CHROME_MOBILE_EMULATION = {"deviceName": "Pixel 2"}
    CHROME_HEADLESS_ARGS = ['--window-size=1920x1080', ]
    FIREFOX_HEADLESS_ARGS = []

    # Functions

    @classmethod
    def get_firefox_driver(cls, headless=False):
        """Returns ``webdriver.Firefox`` object using :attr:`FIREFOX_KWARGS` and :attr:`LOG_PATH` to
        initialize

        :param headless: (Default = False) If True, configure driver to run a
            headless browser
        """
        log_path = os.path.join(cls.LOG_PATH, 'geckodriver.log')
        options = cls._get_firefox_headless_options() if headless else None
        return cls.set_driver_implicit_wait(webdriver.Firefox(log_path=log_path, options=options, **cls.FIREFOX_KWARGS))

    @classmethod
    def get_chrome_driver(cls, headless=False):
        """Returns ``webdriver.Chrome`` object using :attr:`CHROME_KWARGS` and :attr:`LOG_PATH` to
        initialize

        :param headless: (Default = False) If True, configure driver to run a
            headless browser
        """
        service_log_path = os.path.join(cls.LOG_PATH, 'chromedriver.log')
        options = cls._get_chrome_headless_options() if headless else None
        return cls.set_driver_implicit_wait(webdriver.Chrome(service_log_path=service_log_path, options=options,
                                                             **cls.CHROME_KWARGS))

    @classmethod
    def get_safari_driver(cls):
        """Returns ``webdriver.Safari`` object using :attr:`SAFARI_KWARGS` to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Safari(**cls.SAFARI_KWARGS))

    @classmethod
    def get_ie_driver(cls):
        """Returns ``webdriver.Ie`` object using :attr:`IE_KWARGS` and :attr:`LOG_PATH` to initialize"""
        log_file = os.path.join(cls.LOG_PATH, 'iedriver.log')
        return cls.set_driver_implicit_wait(webdriver.Ie(log_file=log_file, **cls.IE_KWARGS))

    @classmethod
    def get_edge_driver(cls):
        """Returns ``webdriver.Edge`` object using :attr:`EDGE_KWARGS` and :attr:`LOG_PATH` to initialize"""
        log_path = os.path.join(cls.LOG_PATH, 'edgedriver.log')
        return cls.set_driver_implicit_wait(webdriver.Edge(log_path=log_path, **cls.EDGE_KWARGS))

    @classmethod
    def get_chrome_mobile_driver(cls, headless=False):
        """Returns ``webdriver.Chrome`` object using :attr:`CHROME_KWARGS`, :attr:`LOG_PATH`, and
        :attr:`CHROME_MOBILE_EMULATION` to initialize

        :param headless: (Default = False) If True, configure driver to run a
            headless browser
        """
        service_log_path = os.path.join(cls.LOG_PATH, 'mobile_chromedriver.log')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", cls.CHROME_MOBILE_EMULATION)
        if headless:
            options.add_argument('--headless')
        return cls.set_driver_implicit_wait(webdriver.Chrome(service_log_path=service_log_path, options=options,
                                                             **cls.CHROME_KWARGS))

    # Driver Options

    @classmethod
    def _get_firefox_headless_options(cls):
        """Returns FirefoxOptions with -headless argument and arguments from
        FIREFOX_HEADLESS_ARGS set
        """
        options = webdriver.FirefoxOptions()
        for arg in cls.FIREFOX_HEADLESS_ARGS:
            options.add_argument(arg)
        options.add_argument('-headless')
        return options

    @classmethod
    def _get_chrome_headless_options(cls):
        """Returns ChromeOptions with --headless argument and arguments from
        CHROME_HEADLESS_ARGS set
        """
        options = webdriver.ChromeOptions()
        for arg in cls.CHROME_HEADLESS_ARGS:
            options.add_argument(arg)
        options.add_argument('--headless')
        return options

    @classmethod
    def set_driver_implicit_wait(cls, driver):
        """Returns driver with implicit wait time set"""
        if cls.IMPLICIT_WAIT > 0:
            driver.implicitly_wait(cls.IMPLICIT_WAIT)
        return driver

    # Misc

    @classmethod
    def new_screenshot_file(cls, browser_name, test_name):
        """Return the full filepath and filename for the screenshot

        :param browser_name: Name of the browser (for screenshot filename)
        :param test_name: Name of the current test (for screenshot filename)

        :return: Filename for the screenshot
        """
        filename_fmt = '{time}-{browser}-{test}.png'
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        filename = filename_fmt.format(time=timestamp, browser=browser_name, test=test_name)
        # Validate string characters for file name
        return os.path.join(cls.SCREENSHOT_PATH, utils.validate_filename(filename))
