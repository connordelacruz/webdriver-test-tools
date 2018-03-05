# Custom expected condition classes

# Imports
# ----------------------------------------------------------------
from webdriver_test_tools import test


class element_is_in_view(object):
    """Custom wait condition for WebDriverWait() that uses JavaScript to check if an element is scrolled into view"""
    def __init__(self, locator, fully_in_view=False):
        self.locator = locator
        self.fully_in_view = fully_in_view

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        return test.is_scrolled_into_view(driver, element, self.fully_in_view)

