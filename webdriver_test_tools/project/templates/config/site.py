from webdriver_test_tools.config import site


class SiteConfig(site.SiteConfig):
    """URL configurations for a site

    :var SiteConfig.SITE_URL: URL of the home page
    :var SiteConfig.BASE_URL: Base URL for site pages (followed by a '/')
    """
    SITE_URL = ''
    BASE_URL = ''
    # DECLARE ANY OTHER URL VARIABLES NEEDED FOR TESTING HERE
