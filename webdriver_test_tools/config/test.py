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

    def get_runner(self):
        """Returns RUNNER_CLASS object using RUNNER_KWARGS to initialize"""
        return self.RUNNER_CLASS(**self.RUNNER_KWARGS)

