import webdriver_test_tools
from webdriver_test_tools import config
import os.path
import page_object_tests


class WebDriverConfig(config.WebDriverConfig):
    """Configurations for webdriver"""

    # File Path Configurations

    # Used to set LOG_PATH and SCREENSHOT_PATH. Do not modify!
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(page_object_tests.__file__))

    # Path to the log directory. Defaults to the log subdirectory in the
    # webdriver_test_tools package root directory if unspecified
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')

    # Path to the screenshot directory. Defaults to the screenshot subdirectory
    # in the webdriver_test_tools package root directory if unspecified
    SCREENSHOT_PATH = os.path.join(_PACKAGE_ROOT, 'screenshot')


    # UNCOMMENT TO OVERRIDE DEFAULT CONFIGURATIONS

    # Browser Driver Initialization Arguments
    #
    # NOTE: Logging configurations are set when the corresponding
    # get_<browser>_driver() method is called. This allows for projects to
    # override the LOG_PATH variable without having to also override all
    # <browser>_KWARGS variables as well.

    # Keyword args for webdriver.Firefox()
    # FIREFOX_KWARGS = {}

    # Keyword args for webdriver.Chrome()
    # CHROME_KWARGS = {}

    # Keyword args for webdriver.Safari()
    # SAFARI_KWARGS = {}

    # Keyword args for webdriver.Ie()
    # IE_KWARGS = {}

    # Keyword args for webdriver.Edge()
    # EDGE_KWARGS = {}


    # Mobile Configurations

    # Dictionary with 'mobileEmulation' options for Chrome
    # CHROME_MOBILE_EMULATION = { "deviceName": "Pixel 2" }


    # Headless Browser Configurations

    # Command line arguments to use in addition to the --headless flag
    # CHROME_HEADLESS_ARGS = ['--window-size=1920x1080',]

    # Command line arguments to use in addition to the -headless flag
    # FIREFOX_HEADLESS_ARGS = []


    # Misc Selenium WebDriver Configurations

    # Implicit wait time for webdriver to poll DOM
    #
    # NOTE: Documentation says not to mix this with explicit waits and some
    # instability was noticed when it was set to 10. Projects can override this
    # if necessary. Implicit wait documentation:
    # https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#explicit-and-implicit-waits
    # IMPLICIT_WAIT = 0

