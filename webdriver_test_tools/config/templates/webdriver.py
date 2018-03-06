# Project configurations for webdriver

from webdriver_test_tools.config import webdriver


class WebDriverConfig(webdriver.WebDriverConfig):
    # UNCOMMENT TO OVERRIDE DEFAULT CONFIGURATIONS

    # Static Configurations
    # ----------------------------------------------------------------
    # Path to the log directory. webdriver.WebDriverConfig uses this variable to set log paths for each browser driver
    # when initialized, so only this variable needs to be updated to account for all drivers.
    # LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')

    # Implicit wait time for webdriver to poll DOM
    # IMPLICIT_WAIT = 10

    # Firefox webdriver initialization arguments
    # FIREFOX_KWARGS = {}

    # Chrome webdriver initialization arguments
    # CHROME_KWARGS = {}

    # Safari webdriver initialization arguments
    # SAFARI_KWARGS = {}

    # Runtime Configurations
    # ----------------------------------------------------------------
    def __init__(self):
        super().__init__()
        # Add any additional configurations that need to be overridden at runtime

