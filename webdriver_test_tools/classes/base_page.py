# Base class for page objects


class BasePage(object):
    """Base class for page objects"""

    def __init__(self, driver):
        """Initialize page object

        :param driver: Selenium WebDriver object
        """
        self.driver = driver


    def find_element(self, locator):
        """Returns a WebElement object based on the locator tuple passed

        Shorthand for ``self.driver.find_element(*locator)``

        :param locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)

        :rtype: WebElement
        """
        return self.driver.find_element(*locator)


    def find_elements(self, locator):
        """Returns a list of WebElement objects based on the locator tuple passed

        Shorthand for ``self.driver.find_elements(*locator)``

        :param locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)

        :rtype: List of WebElement
        """
        return self.driver.find_elements(*locator)

