# IMPORT PAGE OBJECTS HERE

import webdriver_test_tools
from webdriver_test_tools.testcase import *
from framework_tests import config
from selenium import webdriver


# Test Case Classes

class TemplateTestCase(WebDriverTestCase):
    """DESCRIPTION OF TEST CASE HERE"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL

    # Test Methods

