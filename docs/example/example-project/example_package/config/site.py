# URL configurations for a site

from webdriver_test_tools.config import site


class SiteConfig(site.SiteConfig):
    # URL of the home page
    SITE_URL = 'https://www.example.com'
    # Base URL for site pages (followed by a '/')
    BASE_URL = SITE_URL + '/'
    # DECLARE ANY OTHER URL VARIABLES NEEDED FOR TESTING HERE
    # URL linked to by the 'More Information' link on example.com
    INFO_URL = 'https://www.iana.org/domains/reserved'
