# IMPORT PAGE OBJECTS HERE

import webdriver_test_tools
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase, WebDriverMobileTestCase, Browsers
from test_project import config
from selenium import webdriver


# Test Case Classes

class TemplateTestCase(WebDriverTestCase):
    """DESCRIPTION OF TEST CASE HERE"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL

    # Test Methods

