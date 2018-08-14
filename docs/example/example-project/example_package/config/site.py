from webdriver_test_tools.config import site


class SiteConfig(site.SiteConfig):
    """URL configurations for a site

    :var SiteConfig.SITE_URL: URL of the home page
    :var SiteConfig.BASE_URL: Base URL for site pages (followed by a '/')
    """
    SITE_URL = 'https://example.com'
    BASE_URL = SITE_URL + '/'
    # DECLARE ANY OTHER URL VARIABLES NEEDED FOR TESTING HERE
    # URL linked to by the 'More Information' link on example.com
    INFO_URL = 'https://www.iana.org/domains/reserved'
