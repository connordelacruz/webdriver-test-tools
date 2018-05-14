"""Utility functions for locating elements"""

from selenium.webdriver.common.by import By


def by_element_text(element_text, element_type='*', exact_match=False):
    """Returns a locator that selects an element with the specified text

    :param element_text: The text of the element to locate.
    :param element_type: (Optional) The tag type of the element. If unspecified, will
        search all tag types for the specified text.
    :param exact_match: (Default = False) If True, will only match elements with the
        exact string as its text. If False, match elements whose text contains the
        specified string but may also contain other text.

    :return: Locator selecting elements by the specified text
    """
    select_expression_format = 'text()={text}' if exact_match else 'contains(text(), "{text}")'
    xpath_format = '//{tag_type}[{select_expr}]'
    select_expression = select_expression_format.format(text=element_text)
    element_xpath = xpath_format.format(tag_type=element_type, select_expr=select_expression)
    return By.XPATH, element_xpath


def input_elements(exclude_buttons=False):
    """Return a locator that selects ``input``, ``select``, ``textarea``, and (optionally)
    ``button`` elements

    To narrow down results, this is best used on the conainer element where the desired
    inputs are located. E.g.:

    .. code-block:: python

        form_element = driver.find_element_by_id('form-id')
        input_elements = form_element.find_elements(*locate.input_elements())

    :param exclude_buttons: (Default = False) If set to True, omit button elements from
        selector

    :return: Locator selecting input elements
    """
    css_string = 'input,select,textarea'
    if not exclude_buttons:
        css_string += ',button'
    return By.CSS_SELECTOR, css_string


