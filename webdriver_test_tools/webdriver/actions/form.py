"""Helper functions for interacting with forms

.. note::

    As of version 3.0, the methods in this module for filling/retrieving form
    values have been removed. Use
    :class:`~webdriver_test_tools.pageobject.form.FormObject` instead.
"""

from webdriver_test_tools.webdriver.actions import scroll


# Input helper methods

def toggle_checkbox(driver, checkbox_element):
    """Helper method for toggling checkboxes that may or may not be visible

    If checkbox is visible, just click that element. If it's invisible for
    styling reasons, try to find the corresponding label and click that

    :param driver: Selenium webdriver object
    :param checkbox_element: WebElement for the checkbox to toggle

    :return: True if the checkbox is checked after toggling, False if unchecked
    """
    if checkbox_element.is_displayed():
        element_to_click = checkbox_element
    else:
        # Assuming the checkbox has id attribute since label for attributes
        # must reference it
        checkbox_id = checkbox_element.get_attribute('id')
        label_css = 'label[for="{}"]'.format(checkbox_id)
        element_to_click = driver.find_element_by_css_selector(label_css)
    scroll.to_and_click(driver, element_to_click, False)
    return checkbox_element.is_selected()
