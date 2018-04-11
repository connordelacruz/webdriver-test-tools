from selenium import webdriver
import webdriver_test_tools
import os.path


class WebDriverConfig(object):
    """Configurations for webdriver

    :var WebDriverConfig.LOG_PATH: Path to the log directory. Defaults to the log
        subdirectory in the webdriver_test_tools package root directory
    :var WebDriverConfig.LOG_PATH: Implicit wait time for webdriver to poll DOM
        .. note::

            Documentation says not to mix this with explicit waits and some instability
            was noticed when it was set to 10. Projects can override this if necessary.
            `Implicit wait documentation <https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#explicit-and-implicit-waits>`__

    Browser driver initialization arguments:

    :var WebDriverConfig.FIREFOX_KWARGS:
    :var WebDriverConfig.CHROME_KWARGS:
    :var WebDriverConfig.SAFARI_KWARGS:
    :var WebDriverConfig.IE_KWARGS:
    :var WebDriverConfig.EDGE_KWARGS:

    Mobile configurations:

    :var WebDriverConfig.CHROME_MOBILE_EMULATION:
    """
    # Root directory of webdriver_test_tools package
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(webdriver_test_tools.__file__))
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')

    IMPLICIT_WAIT = 0

    FIREFOX_KWARGS = {'log_path': os.path.join(LOG_PATH, 'geckodriver.log')}
    CHROME_KWARGS = {'service_log_path': os.path.join(LOG_PATH, 'chromedriver.log')}
    SAFARI_KWARGS = {}
    IE_KWARGS = {}
    EDGE_KWARGS = {}

    CHROME_MOBILE_EMULATION = { "deviceName": "Pixel 2" }

    # Functions

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
    def get_chrome_mobile_driver(cls):
        """Returns webdriver.Chrome object using CHROME_KWARGS and CHROME_MOBILE_EMULATION to initialize"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", cls.CHROME_MOBILE_EMULATION)
        return cls.set_driver_implicit_wait(webdriver.Chrome(options=options, **cls.CHROME_KWARGS))

    @classmethod
    def set_driver_implicit_wait(cls, driver):
        """Returns driver with implicit wait time set"""
        if cls.IMPLICIT_WAIT > 0:
            driver.implicitly_wait(cls.IMPLICIT_WAIT)
        return driver


