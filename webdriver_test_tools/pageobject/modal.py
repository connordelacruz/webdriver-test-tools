import inspect
from selenium.common.exceptions import NoSuchElementException

from webdriver_test_tools.pageobject import utils, BasePage, YAMLParsingPageObject
from webdriver_test_tools.webdriver import actions


class ModalObject(YAMLParsingPageObject):
    """Page object prototype for modals

    Subclasses should set the following attributes:

    :var ModalObject.YAML_FILE: Path to a YAML file representing the modal
        object. This file is parsed during initialization using
        :meth:`parse_yaml` and is used to determine :attr:`MODAL_LOCATOR` and
        :attr:`CLOSE_LOCATOR`
    :var ModalObject.MODAL_BODY_CLASS: (Optional) Page object for the contents
        of the modal body. If set to a subclass of :class:`BasePage
        <webdriver_test_tools.pageobject.base.BasePage>`,
        :meth:`get_modal_body()` will return an instance of this object.

    The following attributes are determined based on the contents of
    :attr:`YAML_FILE` (or should be set in subclasses if :attr:`YAML_FILE` is
    ``None``):

    :var ModalObject.MODAL_LOCATOR: Locator for the modal element. Override in
        subclasses
    :var ModalObject.CLOSE_LOCATOR: Locator for the close button. Override in
        subclasses
    """

    _YAML_ROOT_KEY = 'modal'
    # Locators
    MODAL_LOCATOR = None
    CLOSE_LOCATOR = None
    # Optional page object for the modal body content
    MODAL_BODY_CLASS = None

    def parse_yaml(self, file_path):
        """Parse a YAML representation of the modal object and set attributes
        accordingly

        See :ref:`YAML ModalObjects doc <yaml-modal-objects>` for details on
        syntax.

        :param file_path: Full path to the YAML file
        """
        parsed_yaml = super().parse_yaml(file_path)
        # Initialize locators
        try:
            self.MODAL_LOCATOR = utils.yaml.parse_locator_dict(parsed_yaml['modal_locator'])
            self.CLOSE_LOCATOR = utils.yaml.parse_locator_dict(parsed_yaml['close_locator'])
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                'Missing required {} key in modal YAML'.format(e)
            )

    def is_displayed(self):
        """Check if the modal is displayed

        This method checks if the element located by :attr:`MODAL_LOCATOR`
        exists and is visible. This should be sufficient for many common
        implementations of modals, but can be overridden if this isn't a
        reliable detection method for an implementation

        :return: True if the modal is displayed, False otherwise
        """
        try:
            displayed = self.find_element(self.MODAL_LOCATOR).is_displayed()
        except NoSuchElementException:
            displayed = False
        return displayed

    def click_close_button(self):
        """Click the modal close button"""
        actions.scroll.to_and_click(self.driver, self.find_element(self.CLOSE_LOCATOR))

    def get_modal_body(self):
        """If :attr:`self.MODAL_BODY_CLASS <MODAL_BODY_CLASS>` is set to a
        subclass of :class:`BasePage
        <webdriver_test_tools.pageobject.base.BasePage>`, returns an instance
        of that object. Otherwise, returns None
        """
        return self.MODAL_BODY_CLASS(self.driver) if inspect.isclass(self.MODAL_BODY_CLASS) and issubclass(self.MODAL_BODY_CLASS, BasePage) else None

