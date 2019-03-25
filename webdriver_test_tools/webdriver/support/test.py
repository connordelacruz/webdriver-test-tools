"""Functions for commonly repeated test procedures"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_test_tools.webdriver.support import expected_conditions as customEC


# Expected Condition Tests

def expected_condition_test(driver, ec_object, wait_timeout=10):
    """Test for an expected condition until wait timeout is reached

    :param driver: Selenium WebDriver object
    :param ec_object: Expected condition object
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out

    :return: True if expected condition occurred, otherwise False
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

    :param driver: Selenium WebDriver object
    :param target_locator: Tuple in the format (by,selector) used to locate target
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out

    :return: True if target is scrolled into view before timeout, False otherwise
    """
    in_view_checker = customEC.element_to_be_in_view(target_locator)
    return expected_condition_test(driver, in_view_checker, wait_timeout)


def visibility_change_test(driver, target_locator, test_visible=True, wait_timeout=10):
    """Expected condition test for visibility changes (e.g. modals)

    :param driver: Selenium WebDriver object
    :param target_locator: Tuple in the format (by,selector) used to locate target
    :param test_visible: (Default=True) An optional variable describing what the
        visibility change is supposed to be. If True, test if the target becomes
        visible. If False, test if the target becomes invisible
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out

    :return: True if the target's visibily changes as expected, False otherwise
    """
    # Determine what EC to use based on test_visible
    visibility_checker = EC.visibility_of_element_located(target_locator) if test_visible else EC.invisibility_of_element_located(target_locator)
    return expected_condition_test(driver, visibility_checker, wait_timeout)


def url_change_test(driver, expected_url, wait_timeout=10):
    """Expected condition test for URL change

    :param driver: Selenium WebDriver object
    :param expected_url: The expected URL
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out

    :return: True if the current URL matches the expected URL before timeout, False
        otherwise
    """
    url_checker = EC.url_to_be(expected_url)
    return expected_condition_test(driver, url_checker, wait_timeout)


def base_url_change_test(driver, expected_url, ignore_trailing_slash=True, wait_timeout=10):
    """Expected condition test for URL change. Ignores query strings in current url

    :param driver: Selenium WebDriver object
    :param expected_url: The expected base URL
    :param ignore_trailing_slash: (Default = True) If True, ignore trailing '/'
        in the expected url and current base URL when comparing
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out

    :return: True if the current URL (ignoring query strings) matches the expected URL
        before timeout, False otherwise
    """
    url_checker = customEC.base_url_to_be(expected_url, ignore_trailing_slash=ignore_trailing_slash)
    return expected_condition_test(driver, url_checker, wait_timeout)


def existence_change_test(driver, target_locator, test_exists=True, wait_timeout=10):
    """Expected condition test for element existence changes (e.g. element that
    gets added/removed dynamically)

    :param driver: Selenium WebDriver object
    :param target_locator: Tuple in the format (by,selector) used to locate target
    :param test_exists: (Default = True) An optional variable describing what
        the existence change is supposed to be. If True, test if the target does
        exist. If False, test if the target no longer exists
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out

    :return: True if the existence of the target changes as expected, False
        otherwise
    """
    exists_checker = customEC.element_to_exist(target_locator) if test_exists else customEC.element_to_not_exist(target_locator)
    return expected_condition_test(driver, exists_checker, wait_timeout)


def enabled_state_change_test(driver, target_locator, test_enabled=True, wait_timeout=10):
    """Expected condition test for element enabled/disabled state changes

    :param driver: Selenium WebDriver object
    :param target_locator: Tuple in the format (by,selector) used to locate target
    :param test_enabled: (Default = True) An optional variable describing what
        the enabled/disabled state change is supposed to be. If True, test if
        the target is enabled. If False, test if the target is disabled
    :param wait_timeout: (Default = 10) Number of seconds to wait for expected
        conditions to occur before timing out
    """
    enabled_checker = customEC.element_to_be_enabled(target_locator) if test_enabled else customEC.element_to_be_disabled(target_locator)
    return expected_condition_test(driver, enabled_checker, wait_timeout)

