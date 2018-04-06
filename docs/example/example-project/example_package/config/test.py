from webdriver_test_tools.config import test


class TestSuiteConfig(test.TestSuiteConfig):
    """Configurations for test suite

    :var TestSuiteConfig.RUNNER_CLASS: unittest TestRunner class to use when running
        tests
    :var TestSuiteConfig.RUNNER_KWARGS: Dictionary mapping parameter names to desired
        values used to initialize the TestRunner
    """
    # UNCOMMENT TO OVERRIDE DEFAULT CONFIGURATIONS
    # RUNNER_CLASS = ColourTextTestRunner
    # RUNNER_KWARGS = {'verbosity': 2}
    pass

