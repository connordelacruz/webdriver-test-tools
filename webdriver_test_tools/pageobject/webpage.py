from webdriver_test_tools.pageobject import BasePage


class WebPageObject(BasePage):
    """Page object prototype for web pages

    :var PAGE_FILENAME: File name of the page relative to
        ``<test_package>.config.SiteConfig.BASE_URL``
    """

    PAGE_FILENAME = None

    def get_page_title(self):
        """Get the title of the current page

        :return: Title of the current page
        """
        return self.driver.get_title()

