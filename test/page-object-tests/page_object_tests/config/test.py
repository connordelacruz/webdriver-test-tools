from webdriver_test_tools.config import test


class TestSuiteConfig(test.TestSuiteConfig):
    """Configurations for test suite"""

    # UNCOMMENT TO OVERRIDE DEFAULT CONFIGURATIONS

    # unittest.TestRunner class to use when running tests
    # RUNNER_CLASS = ColourTextTestRunner

    # Dictionary mapping parameter names to desired values used to initialize
    # the TestRunner configured in RUNNER_CLASS
    # RUNNER_KWARGS = {}

    # Value used if the verbosity parameter is unspecified when calling
    # get_runner()
    # DEFAULT_VERBOSITY = 2

    pass
