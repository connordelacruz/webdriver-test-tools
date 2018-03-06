#!/usr/bin/env python3


# Imports
# ----------------------------------------------------------------
"""IMPORT PAGE OBJECTS HERE"""

import webdriver_test_tools
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase
# TODO: fix config import location
from webdriver_test_tools import config
from selenium import webdriver


# Test Case Classes
# ----------------------------------------------------------------

class TemplateTestCase(WebDriverTestCase):
    """Description of this TestCase"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL

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
    # TODO: pass TestSuiteConfig and WebDriverConfig classes instead
    webdriver_test_tools.test_module.main(tests, config.test.get_runner())
