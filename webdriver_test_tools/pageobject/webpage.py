from webdriver_test_tools.pageobject import BasePage


class WebPageObject(BasePage):
    """Page object prototype for web pages

    :var WebPageObject.PAGE_FILENAME: File name of the page relative to a base
        URL declared in ``SiteConfig``
    :var WebPageObject.PAGE_URL: Full URL of the page (e.g.
        ``SiteConfig.BASE_URL + PAGE_FILENAME``)
    """

    PAGE_FILENAME = None
    PAGE_URL = None

    def get_page_title(self):
        """Get the title of the current page

        :return: Title of the current page
        """
        return self.driver.get_title()

