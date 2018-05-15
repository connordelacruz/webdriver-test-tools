from webdriver_test_tools.pageobject import BasePage
from webdriver_test_tools.webdriver import actions


class FormObject(BasePage):
    """Page object prototype for forms

    :var FORM_LOCATOR: Locator for the form element. Override in subclasses
    :var SUBMIT_LOCATOR: Locator for the submit button. Override in subclasses
    :var SUBMIT_SUCCESS_CLASS: (Optional) Page object of modal/webpage/etc that
        should appear on successful form submission. If subclass set to a subclass of
        :class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>`,
        :meth:`click_submit()` will return an instance of this object.
    """

    # Locators
    FORM_LOCATOR = None
    SUBMIT_LOCATOR = None
    # Optional page object to return on click_submit()
    SUBMIT_SUCCESS_CLASS = None

    class Input:
        """Subclass used to contain name attributes and select/radio option lists for
        inputs

        :Example:

            .. code:: python

                SOME_INPUT = 'someInput'

                SOME_SELECT = 'someSelect'
                SOME_SELECT_OPTIONS = [
                        'vaule1',
                        'value2',
                ]

        """
        pass

    def fill_form(self, input_map):
        """Fill the form element inputs

        :param input_map: Dictionary mapping input names to the values to set them to.
            See :func:`webdriver_test_tools.webdriver.actions.form.fill_form_input`
            for values to use for different input types
        """
        form = self.find_element(self.FORM_LOCATOR)
        actions.form.fill_form_inputs(self.driver, form, input_map)

    def submit_is_enabled(self):
        """Short hand function for checking if the submit button is enabled. Useful
        for forms with JavaScript input validation

        :return: True if submit is enabled, False if it's disabled
        """
        return self.find_element(self.SUBMIT_LOCATOR).is_enabled()

    def click_submit(self):
        """Shorthand function for scrolling to the submit button and clicking it.

        If :attr:`self.SUBMIT_SUCCESS_CLASS <SUBMIT_SUCCESS_CLASS>` is set to a subclass of
        :class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>`,
        an instance of that object will be returned
        """
        submit_button = self.find_element(self.SUBMIT_LOCATOR)
        actions.scroll.to_and_click(self.driver, submit_button, False)
        if issubclass(self.SUBMIT_SUCCESS_CLASS, BasePage):
            return self.SUBMIT_SUCCESS_CLASS(self.driver)

