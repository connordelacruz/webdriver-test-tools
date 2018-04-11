import webdriver_test_tools
from webdriver_test_tools import config
import os.path
import {{test_package}}


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

    :var WebDriverConfig.FIREFOX_KWARGS:
    :var WebDriverConfig.CHROME_KWARGS:
    :var WebDriverConfig.SAFARI_KWARGS:
    :var WebDriverConfig.IE_KWARGS:
    :var WebDriverConfig.EDGE_KWARGS:

    Mobile configurations:

    :var WebDriverConfig.CHROME_MOBILE_EMULATION:
    """

    _PACKAGE_ROOT = os.path.dirname(os.path.abspath({{test_package}}.__file__))
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')

    # UNCOMMENT TO OVERRIDE DEFAULT CONFIGURATIONS

    # IMPLICIT_WAIT = 0

    # FIREFOX_KWARGS = {'log_path': os.path.join(LOG_PATH, 'geckodriver.log')}
    # CHROME_KWARGS = {'service_log_path': os.path.join(LOG_PATH, 'chromedriver.log')}
    # SAFARI_KWARGS = {}
    # IE_KWARGS = {}
    # EDGE_KWARGS = {}

    # CHROME_MOBILE_EMULATION = { "deviceName": "Pixel 2" }

