from colour_runner.runner import ColourTextTestRunner


class TestSuiteConfig(object):
    """Configurations for test suite

    :var TestSuiteConfig.RUNNER_CLASS: ``unittest.TestRunner`` class to use when running
        tests
    :var TestSuiteConfig.RUNNER_KWARGS: Dictionary mapping parameter names to desired
        values used to initialize the ``TestRunner`` configured in :attr:`RUNNER_CLASS`
    """

    # Configure test runner
    RUNNER_CLASS = ColourTextTestRunner
    RUNNER_KWARGS = {}
    # TODO: document
    DEFAULT_VERBOSITY = 2

    # Functions

    # TODO: update to handle --verbosity arg
    @classmethod
    def get_runner(cls, verbosity=None):
        """Returns :attr:`RUNNER_CLASS` object using :attr:`RUNNER_KWARGS` to
        initialize
        """
        if verbosity is None:
            verbosity = cls.DEFAULT_VERBOSITY
        return cls.RUNNER_CLASS(verbosity=verbosity, **cls.RUNNER_KWARGS)

