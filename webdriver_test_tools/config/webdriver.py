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

    # Runtime Configurations
    # ----------------------------------------------------------------
    def __init__(self):
        # Firefox webdriver initialization arguments
        self.FIREFOX_KWARGS = {'log_path': os.path.join(self.LOG_PATH, 'geckodriver.log')}
        # Chrome webdriver initialization arguments
        self.CHROME_KWARGS = {'service_log_path': os.path.join(self.LOG_PATH, 'chromedriver.log')}
        # Safari webdriver initialization arguments
        self.SAFARI_KWARGS = {}

    # Functions
    # ----------------------------------------------------------------

    # Web Drivers
    # --------------------------------

    def get_firefox_driver(self):
        """Returns webdriver.Firefox object using FIREFOX_KWARGS to initialize"""
        return webdriver.Firefox(**self.FIREFOX_KWARGS)

    def get_chrome_driver(self):
        """Returns webdriver.Chrome object using CHROME_KWARGS to initialize"""
        return webdriver.Chrome(**self.CHROME_KWARGS)

    def get_safari_driver(self):
        """Returns webdriver.Safari object using SAFARI_KWARGS to initialize"""
        return webdriver.Safari(**self.SAFARI_KWARGS)


