# Configurations for test suite

from colour_runner.runner import ColourTextTestRunner

# Configurations
# ----------------------------------------------------------------

# Configure test runner
RUNNER_CLASS = ColourTextTestRunner
RUNNER_KWARGS = {'verbosity': 2}

# Functions
# ----------------------------------------------------------------

def get_runner():
    """Returns RUNNER_CLASS object using RUNNER_KWARGS to initialize"""
    return RUNNER_CLASS(**RUNNER_KWARGS)
