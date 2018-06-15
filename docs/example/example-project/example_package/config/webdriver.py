import webdriver_test_tools
from webdriver_test_tools import config
import os.path
import example_package


class WebDriverConfig(config.WebDriverConfig):
    """Configurations for webdriver

    :var WebDriverConfig.LOG_PATH: Path to the log directory. Defaults to the log
        subdirectory in the webdriver_test_tools package root directory
    :var WebDriverConfig.LOG_PATH: Implicit wait time for webdriver to poll DOM
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

    Headless browser configurations:

    :var WebDriverConfig.CHROME_HEADLESS_ARGS: Command line arguments to use in addition to the --headless flag
    :var WebDriverConfig.FIREFOX_HEADLESS_ARGS: Command line arguments to use in addition to the -headless flag
    """

    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(example_package.__file__))
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')

    # UNCOMMENT TO OVERRIDE DEFAULT CONFIGURATIONS

    # IMPLICIT_WAIT = 0

    # FIREFOX_KWARGS = {}
    # CHROME_KWARGS = {}
    # SAFARI_KWARGS = {}
    # IE_KWARGS = {}
    # EDGE_KWARGS = {}

    # CHROME_MOBILE_EMULATION = { "deviceName": "Pixel 2" }
    # CHROME_HEADLESS_ARGS = ['--window-size=1920x1080',]
    # FIREFOX_HEADLESS_ARGS = []