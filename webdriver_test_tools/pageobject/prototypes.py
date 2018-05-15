"""Subclasses of BasePage with additional functions for convenience.

These classes define common operations and attributes for various common components.
These can be subclassed in test projects if useful.

This module imports the following classes:

    :class:`webdriver_test_tools.pageobject.form.FormObject`
    :class:`webdriver_test_tools.pageobject.modal.ModalObject`
    :class:`webdriver_test_tools.pageobject.nav.CollapsibleNavObject`
    :class:`webdriver_test_tools.pageobject.nav.NavObject`
    :class:`webdriver_test_tools.pageobject.webpage.WebPageObject`
"""

from .webpage import WebPageObject
from .nav import NavObject, CollapsibleNavObject
from .form import FormObject
from .modal import ModalObject

