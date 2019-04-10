from webdriver_test_tools.config import site

import os
from urllib import parse

config_dir = os.path.dirname(os.path.abspath(__file__))
# webdriver-test-tools/test/ is 3 levels up and has subdirectory html
test_html_dir = os.path.abspath(
    os.path.join(config_dir, *tuple(os.pardir for i in range(3)), 'html')
)
# use file:// protocol
# TODO: More reliable means of converting path to url
test_base_url = 'file://' + parse.quote(test_html_dir) + '/'


class SiteConfig(site.SiteConfig):
    """URL configurations for a site"""
    # URL of the home page
    SITE_URL = test_base_url
    # Base URL for site pages (followed by a '/')
    BASE_URL = SITE_URL

    # DECLARE ANY OTHER URL VARIABLES NEEDED FOR TESTING HERE
