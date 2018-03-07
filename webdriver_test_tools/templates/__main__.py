#!/usr/bin/env python3

import webdriver_test_tools
from {{test_package}} import config
# UNCOMMENT AND IMPORT TEST MODULES
# from {{test_package}}.tests import


# TODO: auto load classes from tests.*
def test_list():
    """Returns a list with the contents of each module's tests list added to it"""
    tests = []
    # Add tests from each module
    # EXTEND LIST AS NEW MODULES ARE ADDED E.G.:
    # tests.extend(<module>.tests)
    return tests


if __name__ == '__main__':
    webdriver_test_tools.test_module.main(test_list(), config.TestSuiteConfig.get_runner())
