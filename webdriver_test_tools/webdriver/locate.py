# Utility functions for locating elements

from selenium.webdriver.common.by import By


def by_element_text(element_text, element_type='*', exact_match=False):
    """Returns a locator that selects an element with the specified text

    :param element_text: The text of the element to locate.
    :param element_type: (Optional) The tag type of the element. If unspecified, will search all tag types for the specified text.
    :param exact_match: (Default = False) If True, will only match elements with the exact string as its text. If False, match elements whose text contains the specified string but may also contain other text.

    :return: Locator selecting elements by the specified text
    """
    select_expression_format = 'text()={text}' if exact_match else 'contains(text(), "{text}")'
    xpath_format = '//{tag_type}[{select_expr}]'
    select_expression = select_expression_format.format(text=element_text)
    element_xpath = xpath_format.format(tag_type=element_type, select_expr=select_expression)
    return (By.XPATH, element_xpath)

