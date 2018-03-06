# Configurations for webdriver

from selenium import webdriver
import webdriver_test_tools
import os.path


class WebDriverConfig(object):
    # Root directory of webdriver_test_tools package
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(webdriver_test_tools.__file__))

    # Static Configurations
    # ----------------------------------------------------------------
    # Path to the log directory
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')
    # Implicit wait time for webdriver to poll DOM
    IMPLICIT_WAIT = 10

    # Firefox webdriver initialization arguments
    FIREFOX_KWARGS = {}
    # Chrome webdriver initialization arguments
    CHROME_KWARGS = {}
    # Safari webdriver initialization arguments
    SAFARI_KWARGS = {}

    # Runtime Configurations
    # ----------------------------------------------------------------
    def __init__(self):
        # Add log path at initialization so subclasses only need to override LOG_PATH
        self.FIREFOX_KWARGS['log_path'] = os.path.join(self.LOG_PATH, 'geckodriver.log')
        self.CHROME_KWARGS['service_log_path'] = os.path.join(self.LOG_PATH, 'chromedriver.log')
        # NOTE: Safari driver doesn't have logging options at this time
        # self.SAFARI_KWARGS[] = os.path.join(self.LOG_PATH, 'safaridriver.log')

    # Functions
    # ----------------------------------------------------------------

    # Web Drivers
    # --------------------------------

    def get_firefox_driver(self):
        """Returns webdriver.Firefox object using FIREFOX_KWARGS to initialize"""
        return self.set_driver_implicit_wait(webdriver.Firefox(**self.FIREFOX_KWARGS))

    def get_chrome_driver(self):
        """Returns webdriver.Chrome object using CHROME_KWARGS to initialize"""
        return self.set_driver_implicit_wait(webdriver.Chrome(**self.CHROME_KWARGS))

    def get_safari_driver(self):
        """Returns webdriver.Safari object using SAFARI_KWARGS to initialize"""
        return self.set_driver_implicit_wait(webdriver.Safari(**self.SAFARI_KWARGS))

    def set_driver_implicit_wait(self, driver):
        """Returns driver with implicit wait time set"""
        driver.implicitly_wait(self.IMPLICIT_WAIT)
        return driver


