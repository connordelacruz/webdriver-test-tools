from colour_runner.runner import ColourTextTestRunner


class TestSuiteConfig:
    """Configurations for test suite"""

    #: ``unittest.TestRunner`` class to use when running tests
    RUNNER_CLASS = ColourTextTestRunner
    #: Dictionary mapping parameter names to desired values used to initialize
    #: the ``TestRunner`` configured in :attr:`RUNNER_CLASS`
    RUNNER_KWARGS = {}

    DEFAULT_VERBOSITY = 2
    """Value used if the ``verbosity`` parameter is unspecified when calling
    :meth:`get_runner()`.

    .. note::

        - Conflict may occur if ``'verbosity'`` is set in :attr:`RUNNER_KWARGS`.
          Be sure to use :attr:`DEFAULT_VERBOSITY` instead for setting this
          value.
        - :meth:`get_runner()` assumes the :attr:`RUNNER_CLASS` constructor
          takes a ``verbosity`` parameter in its constructor. If using a custom
          test runner class that doesn't support this, you should override the
          :meth:`get_runner()` method in your project's ``TestSuiteConfig``
          class.
    """

    # Functions

    @classmethod
    def get_runner(cls, verbosity=None):
        """Returns :attr:`RUNNER_CLASS` object using :attr:`RUNNER_KWARGS` to
        initialize

        :param verbosity: (Optional) value to use for the ``verbosity``
            parameter when initializing the test runner. Uses
            :attr:`DEFAULT_VERBOSITY` if unspecified.

        :return: The initialized ``TestRunner`` object
        """
        if verbosity is None:
            verbosity = cls.DEFAULT_VERBOSITY
        return cls.RUNNER_CLASS(verbosity=verbosity, **cls.RUNNER_KWARGS)

