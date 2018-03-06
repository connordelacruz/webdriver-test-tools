#!/usr/bin/env python3


# Imports
# ----------------------------------------------------------------
"""IMPORT PAGE OBJECTS HERE"""

import webdriver_test_tools
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase
# TODO: fix config import location
# TODO: update to use classes
from webdriver_test_tools import config
from selenium import webdriver


# Test Case Classes
# ----------------------------------------------------------------

class TemplateTestCase(WebDriverTestCase):
    """Description of this TestCase"""

    # Test Functions
    # --------------------------------

    """TEST FUNCTIONS HERE"""


# Test Suite
# ----------------------------------------------------------------
"""LIST OF TEST CASE CLASSES HERE"""
tests = [
        TemplateTestCase,
        ]

if __name__ == '__main__':
    webdriver_test_tools.test_module.main(tests, config.test.get_runner())
