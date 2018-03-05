# Functions for commonly repeated test procedures

# Imports
# ----------------------------------------------------------------
from webdriver_test_tools.webdriver.support import expected_conditions as customEC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# Functions
# ----------------------------------------------------------------

# Element Tests
# --------------------------------


def element_exists(driver, element_locator):
    """Returns True if the element exists, False if not

    This function is just a wrapper that catches the NoSuchElementException thrown by
    driver.find_element() and returns a boolean based on whether the exception occurred.
    Used for test assertions.

    :param driver: Selenium webdriver object
    :param element_locator: Tuple in the format (by,selector) used to locate target
    """
    exists = True
    try:
        driver.find_element(*element_locator)
    except NoSuchElementException as e:
        exists = False
    return exists


def is_scrolled_into_view(driver, element, fully_in_view=True):
    """Returns True if the element is scrolled into view, False otherwise

    Currently, Selenium doesn't offer a means of getting an element's location relative
    to the viewport, so using JavaScript to determine whether the element is visible
    within the viewport.

    :param driver: Selenium webdriver object
    :param element: WebElement for the element to check
    :param fully_in_view: (Default = True) If True, check that the element is fully in view and not cut off. If False, check that it's at least partially in view
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


# Expected Condition Tests
# --------------------------------

def expected_condition_test(driver, ec_object, wait_timeout=10):
    """Test for an expected condition until wait timeout is reached

    :param driver: Selenium webdriver object
    :param ec_object: Expected condition object
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected conditions to occur before timing out

    :return: True if expected condition occurred, otherwise False.
    """
    result = True
    try:
        WebDriverWait(driver, wait_timeout).until(ec_object)
    except TimeoutException:
        result = False
    # One last check to ensure expected condition is in place on return
    return result and bool(ec_object(driver))


def in_view_change_test(driver, target_locator, wait_timeout=10):
    """Expected condition test for an element to scroll into view (e.g. same-page link with scroll animation)

    :param driver: Selenium webdriver object
    :param target_locator: Tuple in the format (by,selector) used to locate target
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected conditions to occur before timing out

    :return: True if target is scrolled into view before timeout, False otherwise
    """
    in_view_checker = customEC.element_is_in_view(target_locator)
    return expected_condition_test(driver, in_view_checker, wait_timeout)


def visibility_change_test(driver, target_locator, test_visible=True, wait_timeout=10):
    """Expected condition test for visibility changes (e.g. modals)

    :param driver: Selenium webdriver object
    :param target_locator: Tuple in the format (by,selector) used to locate target
    :param test_visible: (Default=True) An optional variable describing what the visibility change is supposed to be. If True, test if the target becomes visible. If False, test if the target becomes invisible.
    :param wait_timeout: (Default = 10) Number of seconds to wait expected conditions to occur before timing out

    :return: True if the target's visibily changes as expected, False otherwise
    """
    # Determine what EC to use based on test_visible
    visibility_checker = EC.visibility_of_element_located(target_locator) if test_visible else EC.invisibility_of_element_located(target_locator)
    return expected_condition_test(driver, visibility_checker, wait_timeout)


def url_change_test(driver, expected_url, wait_timeout=10):
    """Expected condition test for URL change

    :param driver: Selenium webdriver object
    :param expected_url: The expected URL
    :param wait_timeout: (Default = 10) Number of seconds to wait expected conditions to occur before timing out
    """
    url_checker = EC.url_to_be(expected_url)
    return expected_condition_test(driver, url_checker, wait_timeout)
