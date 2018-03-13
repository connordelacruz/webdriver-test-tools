# Configurations for webdriver

from selenium import webdriver
import webdriver_test_tools
import os.path


class WebDriverConfig(object):
    # Root directory of webdriver_test_tools package
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(webdriver_test_tools.__file__))

    # Configurations
    # ----------------------------------------------------------------
    # Path to the log directory
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')
    # Implicit wait time for webdriver to poll DOM
    # NOTE: Documentation says not to mix this with explicit waits and some instability
    # was noticed when it was set to 10. Leaving this value in for compatibility and for
    # a possible update where projects can override these configs, but it's essentially
    # not used currently.
    # https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#explicit-and-implicit-waits
    IMPLICIT_WAIT = 0

    # Firefox webdriver initialization arguments
    FIREFOX_KWARGS = {'log_path': os.path.join(LOG_PATH, 'geckodriver.log')}
    # Chrome webdriver initialization arguments
    CHROME_KWARGS = {'service_log_path': os.path.join(LOG_PATH, 'chromedriver.log')}
    # Safari webdriver initialization arguments
    SAFARI_KWARGS = {}
    # Internet Explorer webdriver initialization arguments
    IE_KWARGS = {}
    # Edge webdriver initialization arguments
    EDGE_KWARGS = {}

    # Functions
    # ----------------------------------------------------------------

    # Web Drivers
    # --------------------------------

    @classmethod
    def get_firefox_driver(cls):
        """Returns webdriver.Firefox object using FIREFOX_KWARGS to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Firefox(**cls.FIREFOX_KWARGS))

    @classmethod
    def get_chrome_driver(cls):
        """Returns webdriver.Chrome object using CHROME_KWARGS to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Chrome(**cls.CHROME_KWARGS))

    @classmethod
    def get_safari_driver(cls):
        """Returns webdriver.Safari object using SAFARI_KWARGS to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Safari(**cls.SAFARI_KWARGS))

    @classmethod
    def get_ie_driver(cls):
        """Returns webdriver.Ie object using IE_KWARGS to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Ie(**cls.IE_KWARGS))

    @classmethod
    def get_edge_driver(cls):
        """Returns webdriver.Edge object using EDGE_KWARGS to initialize"""
        return cls.set_driver_implicit_wait(webdriver.Edge(**cls.EDGE_KWARGS))

    @classmethod
    def set_driver_implicit_wait(cls, driver):
        """Returns driver with implicit wait time set"""
        if cls.IMPLICIT_WAIT > 0:
            driver.implicitly_wait(cls.IMPLICIT_WAIT)
        return driver


