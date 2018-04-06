from webdriver_test_tools.config import browserstack


# TODO: document when everything is in place
class BrowserStackConfig(browserstack.BrowserStackConfig):
    """Configurations for BrowserStack testing"""

    # Set to True to enable BrowserStack testing
    ENABLE = False
    # Account username. Projects will need to override this
    USERNAME = None
    # Access key. Projects will need to override this
    ACCESS_KEY = None

    # TODO: configure available browsers


