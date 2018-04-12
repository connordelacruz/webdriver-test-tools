from selenium import webdriver
import webdriver_test_tools
import os.path


class WebDriverConfig(object):
    """Configurations for webdriver

    :var WebDriverConfig.LOG_PATH: Path to the log directory. Defaults to the log
        subdirectory in the webdriver_test_tools package root directory
    :var WebDriverConfig.IMPLICIT_WAIT: Implicit wait time for webdriver to poll DOM

        .. note::

            Documentation says not to mix this with explicit waits and some instability
            was noticed when it was set to 10. Projects can override this if necessary.
            `Implicit wait documentation <https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#explicit-and-implicit-waits>`__

    Browser driver initialization arguments:

    :var WebDriverConfig.FIREFOX_KWARGS: Keyword args for webdriver.Firefox()
    :var WebDriverConfig.CHROME_KWARGS: Keyword args for webdriver.Chrome()
    :var WebDriverConfig.SAFARI_KWARGS: Keyword args for webdriver.Safari()
    :var WebDriverConfig.IE_KWARGS: Keyword args for webdriver.Ie()
    :var WebDriverConfig.EDGE_KWARGS: Keyword args for webdriver.Edge()

    .. note::

        Logging configurations are set when the corresponding ``get_<browser>_driver()``
        method is called. This allows for projects to override the ``LOG_PATH`` variable
        without having to also override all ``<browser>_KWARGS`` variables as well.

    Mobile configurations:

    :var WebDriverConfig.CHROME_MOBILE_EMULATION: Dictionary with 'mobileEmulation'
        options for Chrome
    """
    # Root directory of webdriver_test_tools package
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(webdriver_test_tools.__file__))
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')

    IMPLICIT_WAIT = 0

    FIREFOX_KWARGS = {}
    CHROME_KWARGS = {}
    SAFARI_KWARGS = {}
    IE_KWARGS = {}
    EDGE_KWARGS = {}

    CHROME_MOBILE_EMULATION = { "deviceName": "Pixel 2" }

    # Functions

    @classmethod
    def get_firefox_driver(cls):
        """Returns webdriver.Firefox object using FIREFOX_KWARGS and LOG_PATH to
        initialize
        """
        log_path = os.path.join(cls.LOG_PATH, 'geckodriver.log')
        return cls.set_driver_implicit_wait(webdriver.Firefox(log_path=log_path, **cls.FIREFOX_KWARGS))

    @classmethod
    def get_chrome_driver(cls):
        """Returns webdriver.Chrome object using CHROME_KWARGS and LOG_PATH to
        initialize
        """
        service_log_path = os.path.join(cls.LOG_PATH, 'chromedriver.log')
        return cls.set_driver_implicit_wait(webdriver.Chrome(service_log_path=service_log_path, **cls.CHROME_KWARGS))

    @classmethod
    def get_safari_driver(cls):
        """Returns webdriver.Safari object using SAFARI_KWARGS to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Safari(**cls.SAFARI_KWARGS))

    @classmethod
    def get_ie_driver(cls):
        """Returns webdriver.Ie object using IE_KWARGS and LOG_PATH to initialize"""
        log_file = os.path.join(cls.LOG_PATH, 'iedriver.log')
        return cls.set_driver_implicit_wait(webdriver.Ie(log_file=log_file, **cls.IE_KWARGS))

    @classmethod
    def get_edge_driver(cls):
        """Returns webdriver.Edge object using EDGE_KWARGS and LOG_PATH to initialize"""
        log_path = os.path.join(cls.LOG_PATH, 'edgedriver.log')
        return cls.set_driver_implicit_wait(webdriver.Edge(log_path=log_path, **cls.EDGE_KWARGS))

    @classmethod
    def get_chrome_mobile_driver(cls):
        """Returns webdriver.Chrome object using CHROME_KWARGS, LOG_PATH, and
        CHROME_MOBILE_EMULATION to initialize
        """
        service_log_path = os.path.join(cls.LOG_PATH, 'mobile_chromedriver.log')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", cls.CHROME_MOBILE_EMULATION)
        return cls.set_driver_implicit_wait(webdriver.Chrome(service_log_path=service_log_path, options=options, **cls.CHROME_KWARGS))

    @classmethod
    def set_driver_implicit_wait(cls, driver):
        """Returns driver with implicit wait time set"""
        if cls.IMPLICIT_WAIT > 0:
            driver.implicitly_wait(cls.IMPLICIT_WAIT)
        return driver


