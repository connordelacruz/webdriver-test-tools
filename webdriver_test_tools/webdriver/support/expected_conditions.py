"""Custom expected condition classes"""
from selenium.common.exceptions import NoSuchElementException

from . import test
from webdriver_test_tools.common import utils


# TODO: add expected conditions for all basic tests that don't have one
# TODO: add inverse conditions for each? at least for consistency
# TODO: make class names consistent with selenium's absurd naming conventions

class element_to_exist:
    """Custom wait condition for WebdriverWait() that checks if an element
    exists
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return test.element_exists(driver, self.locator)


class element_to_not_exist:
    """Custom wait condition for WebdriverWait() that checks if an element
    does not exists
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return not test.element_exists(driver, self.locator)


class element_to_be_enabled:
    """Custom wait condition for WebdriverWait() that checks if an element
    is enabled
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return driver.find_element(*self.locator).is_enabled()


class element_to_be_disabled:
    """Custom wait condition for WebdriverWait() that checks if an element
    is disabled
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return not driver.find_element(*self.locator).is_enabled()


# TODO: element_to_be_in_view? naming conventions for EC are weird
class element_is_in_view:
    """Custom wait condition for WebDriverWait() that uses JavaScript to check
    if an element is scrolled into view
    """
    def __init__(self, locator, fully_in_view=False):
        self.locator = locator
        self.fully_in_view = fully_in_view

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return test.is_scrolled_into_view(driver, element, self.fully_in_view)


class base_url_to_be:
    """An expectation for checking the current url, ignoring query strings
    (i.e. strips '?' and everything after it and only looks at the base URL)

    url is the expected URL, which must be an exact match with the current base
    URL

    returns True if the base URL matches, false otherwise
    """
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        base_url = utils.get_base_url(driver.current_url)
        return self.url == base_url

