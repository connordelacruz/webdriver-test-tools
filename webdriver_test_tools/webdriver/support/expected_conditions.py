"""Custom expected condition classes"""

from . import test
from webdriver_test_tools.common import utils


class element_is_in_view(object):
    """Custom wait condition for WebDriverWait() that uses JavaScript to check if an
    element is scrolled into view
    """
    def __init__(self, locator, fully_in_view=False):
        self.locator = locator
        self.fully_in_view = fully_in_view

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return test.is_scrolled_into_view(driver, element, self.fully_in_view)


class base_url_to_be(object):
    """An expectation for checking the current url, ignoring query strings (i.e. strips
    '?' and everything after it and only looks at the base URL)

    url is the expected URL, which must be an exact match with the current base URL

    returns True if the base URL matches, false otherwise
    """
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        base_url = utils.get_base_url(driver.current_url)
        return self.url == base_url
