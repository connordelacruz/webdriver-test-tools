
class BasePage:
    """Base class for page objects"""

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.

        :Example:

            .. code-block:: python

                SOME_ELEMENT = (By.ID, 'some-element')

        This nested class is not technically required, but for consistency it's
        recommended to use this convention for storing locators relevant to a
        page object
        """
        pass

    def __init__(self, driver):
        """Initialize page object

        :param driver: Selenium WebDriver object
        """
        self.driver = driver

    def find_element(self, locator):
        """Returns a WebElement object based on the locator tuple passed

        Shorthand for:

            .. code-block:: python

                self.driver.find_element(*locator)

        :param locator: WebDriver locator tuple in the format
            ``(By.<attr>, <locator string>)``

        :return: The located WebElement
        """
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        """Returns a list of WebElement objects based on the locator tuple
        passed

        Shorthand for :

            .. code-block:: python

                self.driver.find_elements(*locator)

        :param locator: WebDriver locator tuple in the format
            ``(By.<attr>, <locator string>)``

        :return: List of located WebElements
        """
        return self.driver.find_elements(*locator)

