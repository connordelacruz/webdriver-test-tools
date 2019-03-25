"""Custom expected condition classes"""
from selenium.common.exceptions import NoSuchElementException

from webdriver_test_tools.common import utils


# TODO: add inverse conditions for each? at least for consistency

# Expected Condition Classes

class element_to_exist:
    """Custom wait condition for WebdriverWait() that checks if an element
    exists
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return _element_exists(driver, self.locator)


class element_to_not_exist:
    """Custom wait condition for WebdriverWait() that checks if an element
    does not exists
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return not _element_exists(driver, self.locator)


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


class element_to_be_in_view:
    """Custom wait condition for WebDriverWait() that uses JavaScript to check
    if an element is scrolled into view
    """
    def __init__(self, locator, fully_in_view=False):
        self.locator = locator
        self.fully_in_view = fully_in_view

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return _is_scrolled_into_view(driver, element, self.fully_in_view)


class base_url_to_be:
    """An expectation for checking the current url, ignoring query strings
    (i.e. strips '?' and everything after it and only looks at the base URL)

    url is the expected URL, which must be an exact match with the current base
    URL

    Optionally accepts the parameter ``ignore_trailing_slash`` (default: True),
    which will strip any trailing '/' from the expected URL and current base
    URL before comparing

    returns True if the base URL matches, false otherwise
    """

    def __init__(self, url, ignore_trailing_slash=True):
        self.url = url
        self.ignore_trailing_slash = ignore_trailing_slash

    def __call__(self, driver):
        base_url = utils.get_base_url(driver.current_url)
        expected_url = self.url
        if self.ignore_trailing_slash:
            expected_url, base_url = self._handle_trailing_slashes(base_url)
        return expected_url == base_url

    def _handle_trailing_slashes(self, base_url):
        """Utility function to strip trailing '/' from the expected URL and
        current base URL

        :param base_url: The current URL with any query strings stripped

        :return: A tuple with (``self.url``, ``base_url``) with any trailing
            '/' removed
        """
        return (self._strip_trailing_slash(self.url),
                self._strip_trailing_slash(base_url))

    def _strip_trailing_slash(self, url):
        if url.endswith('/'):
            url = url[:-1]
        return url


# Helper Methods

def _is_scrolled_into_view(driver, element, fully_in_view=True):
    """Returns True if the element is scrolled into view, False otherwise

    Currently, Selenium doesn't offer a means of getting an element's location relative
    to the viewport, so using JavaScript to determine whether the element is visible
    within the viewport.

    :param driver: Selenium WebDriver object
    :param element: WebElement for the element to check
    :param fully_in_view: (Default = True) If True, check that the element is fully in
        view and not cut off. If False, check that it's at least partially in view

    :return: True if the element is scrolled into view, False otherwise
    """
    # the JavaScript used to check if the element is in view.
    script_string = '''
    return function(el, strict) {
        var rect = el.getBoundingClientRect();
        var elemTop = rect.top;
        var elemBottom = rect.bottom;

        if (strict)
            var isVisible = (elemTop >= 0) && (elemBottom <= window.innerHeight);
        else
            isVisible = elemTop < window.innerHeight && elemBottom >= 0;
        return isVisible;
    }(arguments[0],arguments[1])
    '''
    return driver.execute_script(script_string, element, fully_in_view)


def _element_exists(driver, element_locator):
    """Returns True if the element exists, False if not

    This function is just a wrapper that catches the NoSuchElementException thrown by
    driver.find_element() and returns a boolean based on whether the exception occurred.
    Used for test assertions.

    :param driver: Selenium WebDriver object
    :param element_locator: Tuple in the format (by,selector) used to locate target

    :return: True if the element exists, False if not
    """
    exists = True
    try:
        driver.find_element(*element_locator)
    except NoSuchElementException:
        exists = False
    return exists
