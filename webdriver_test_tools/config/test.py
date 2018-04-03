from colour_runner.runner import ColourTextTestRunner


class TestSuiteConfig(object):
    """Configurations for test suite

    :var TestSuiteConfig.RUNNER_CLASS: unittest TestRunner class to use when running
        tests
    :var TestSuiteConfig.RUNNER_KWARGS: Dictionary mapping parameter names to desired
        values used to initialize the TestRunner
    """

    # Configure test runner
    RUNNER_CLASS = ColourTextTestRunner
    RUNNER_KWARGS = {'verbosity': 2}

    # Functions

    @classmethod
    def get_runner(cls):
        """Returns RUNNER_CLASS object using RUNNER_KWARGS to initialize"""
        return cls.RUNNER_CLASS(**cls.RUNNER_KWARGS)

