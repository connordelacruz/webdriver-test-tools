# Page object

# Imports
# ----------------------------------------------------------------
from webdriver_test_tools.classes.base_page import BasePage
from webdriver_test_tools.webdriver import actions
from selenium.webdriver.common.by import By

# Page Classes
# ----------------------------------------------------------------

class TemplatePage(BasePage):
    # Locators
    # --------------------------------
    class Locator(object):
        """WebDriver locator tuples for any elements that will need to be accessed by
        this page object.

        :Example:

            SOME_ELEMENT = (By.ID, 'some-element')
        """
        pass

    # Input Names
    # --------------------------------
    class Input(object):
        """Put the name attributes of inputs here (if applicable, otherwise the Input
        subclass is not necessary)

        :Example:

            SOME_INPUT = 'someInput'
        """
        pass


    # Page Functions
    # --------------------------------

    """Put functions that interact with page elements here."""

