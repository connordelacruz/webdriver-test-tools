import os
from datetime import datetime

from selenium import webdriver

import webdriver_test_tools
from webdriver_test_tools.common.files import create_directory, validate_filename


class WebDriverConfig:
    """Configurations for webdriver"""
    # Root directory of webdriver_test_tools package
    _PACKAGE_ROOT = os.path.dirname(os.path.abspath(webdriver_test_tools.__file__))
    #: Path to the log directory. Defaults to the log subdirectory in the
    #: ``webdriver_test_tools`` package root directory
    LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')
    #: Path to the screenshot directory. Defaults to the screenshot
    #: subdirectory in the ``webdriver_test_tools`` package root directory
    SCREENSHOT_PATH = os.path.join(_PACKAGE_ROOT, 'screenshot')

    SCREENSHOT_FILENAME_FORMAT = '{date}/{time}-{test}-{browser}.png'
    """Format string used to determine filenames for screenshots (relative to
    :attr:`WebDriverConfig.SCREENSHOT_PATH`). The format string can include the
    following parameters:

        * ``{date}``: Replaced with the date the screenshot was taken
          (YYYY-MM-DD)
        * ``{time}``: Replaced with the time the screenshot was taken
          (HHMMSS)
        * ``{test}``: Replaced with the test method running when screenshot
          was taken
        * ``{browser}``: Replaced with the browser used when screenshot was
          taken

    The format string can include '/' directory separators to save screenshots
    in subdirectories of :attr:`WebDriverConfig.SCREENSHOT_PATH`.
    """

    DEFAULT_ASSERTION_TIMEOUT=10
    """Default number of seconds for :ref:`WebDriverTestCase assertion methods
    <assertion-methods>` to wait for expected conditions to occur before test
    fails
    """

    # Browser driver initialization arguments

    #: Keyword args for ``webdriver.Firefox()``
    FIREFOX_KWARGS = {}
    #: Keyword args for ``webdriver.Chrome()``
    CHROME_KWARGS = {}
    #: Keyword args for ``webdriver.Safari()``
    SAFARI_KWARGS = {}
    #: Keyword args for ``webdriver.Ie()``
    IE_KWARGS = {}
    #: Keyword args for ``webdriver.Edge()``
    EDGE_KWARGS = {}

    # Mobile configurations

    #: Dictionary with 'mobileEmulation' options for Chrome
    CHROME_MOBILE_EMULATION = {"deviceName": "Pixel 2"}

    # Headless browser configurations

    #: Command line arguments to use in addition to the ``--headless`` flag
    CHROME_HEADLESS_ARGS = ['--window-size=1920x1080']
    #: Command line arguments to use in addition to the ``-headless`` flag
    FIREFOX_HEADLESS_ARGS = []


    # Methods

    @classmethod
    def get_firefox_driver(cls, headless=False):
        """Returns ``webdriver.Firefox`` object using :attr:`FIREFOX_KWARGS` and :attr:`LOG_PATH` to
        initialize

        :param headless: (Default = False) If True, configure driver to run a
            headless browser
        """
        log_path = os.path.join(cls.LOG_PATH, 'geckodriver.log')
        options = cls._get_firefox_headless_options() if headless else None
        return webdriver.Firefox(log_path=log_path, options=options,
                                 **cls.FIREFOX_KWARGS)

    @classmethod
    def get_chrome_driver(cls, headless=False):
        """Returns ``webdriver.Chrome`` object using :attr:`CHROME_KWARGS` and :attr:`LOG_PATH` to
        initialize

        :param headless: (Default = False) If True, configure driver to run a
            headless browser
        """
        service_log_path = os.path.join(cls.LOG_PATH, 'chromedriver.log')
        options = cls._get_chrome_headless_options() if headless else None
        return webdriver.Chrome(service_log_path=service_log_path,
                                options=options, **cls.CHROME_KWARGS)

    @classmethod
    def get_safari_driver(cls):
        """Returns ``webdriver.Safari`` object using :attr:`SAFARI_KWARGS` to initialize"""
        return webdriver.Safari(**cls.SAFARI_KWARGS)

    @classmethod
    def get_ie_driver(cls):
        """Returns ``webdriver.Ie`` object using :attr:`IE_KWARGS` and :attr:`LOG_PATH` to initialize"""
        log_file = os.path.join(cls.LOG_PATH, 'iedriver.log')
        return webdriver.Ie(log_file=log_file, **cls.IE_KWARGS)

    @classmethod
    def get_edge_driver(cls):
        """Returns ``webdriver.Edge`` object using :attr:`EDGE_KWARGS` and :attr:`LOG_PATH` to initialize"""
        log_path = os.path.join(cls.LOG_PATH, 'edgedriver.log')
        return webdriver.Edge(log_path=log_path, **cls.EDGE_KWARGS)

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
        return webdriver.Chrome(service_log_path=service_log_path,
                                options=options, **cls.CHROME_KWARGS)

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

    # Misc

    @classmethod
    def new_screenshot_file(cls, browser_name, test_name, makedirs=True):
        """Return the full path and filename for the screenshot

        The filename is determined by the format set in
        :attr:`WebDriverConfig.SCREENSHOT_FILENAME_FORMAT`. If the format doesn't
        end with '.png', the extension will be appended to the resulting
        filename

        :param browser_name: Name of the browser (for screenshot filename)
        :param test_name: Name of the current test (for screenshot filename)
        :param makedirs: (Default = True) If True, create any subdirectories of
            screenshot/ if they don't already exist

        :return: Filename for the screenshot
        """
        now = datetime.now()
        path = cls.SCREENSHOT_FILENAME_FORMAT.format(
            date=now.strftime('%Y-%m-%d'),
            time=now.strftime('%H%M%S'),
            test=test_name,
            browser=browser_name
        )
        # Ensure .png extension is present
        if not path.lower().endswith('.png'):
            path += '.png'
        # Validate string characters for file name
        filename = validate_filename(os.path.basename(path))
        # Get any subdirectory names
        dirname = os.path.dirname(path)
        # Create subdirectories if they don't already exist
        if makedirs:
            create_directory(cls.SCREENSHOT_PATH, dirname)
        return os.path.join(cls.SCREENSHOT_PATH, dirname, filename)

