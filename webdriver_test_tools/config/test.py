# Configurations for test suite

from colour_runner.runner import ColourTextTestRunner


class TestSuiteConfig(object):
    # Configurations
    # ----------------------------------------------------------------
    # Configure test runner
    RUNNER_CLASS = ColourTextTestRunner
    RUNNER_KWARGS = {'verbosity': 2}

    # Functions
    # ----------------------------------------------------------------

    @classmethod
    def get_runner(cls):
        """Returns RUNNER_CLASS object using RUNNER_KWARGS to initialize"""
        return cls.RUNNER_CLASS(**cls.RUNNER_KWARGS)

