"""Subclasses of BasePage with additional functions for convenience.

These classes define common operations and attributes for various common
components.  These can be subclassed in test projects if useful.

This module imports the following classes:

    :class:`webdriver_test_tools.pageobject.form.FormObject`
    :class:`webdriver_test_tools.pageobject.form.InputObject`
    :class:`webdriver_test_tools.pageobject.modal.ModalObject`
    :class:`webdriver_test_tools.pageobject.nav.NavLinkObject`
    :class:`webdriver_test_tools.pageobject.nav.NavMenuObject`
    :class:`webdriver_test_tools.pageobject.nav.NavObject`
    :class:`webdriver_test_tools.pageobject.webpage.WebPageObject`

The following deprecated classes are also imported, but may be removed in
future versions:

    :class:`webdriver_test_tools.pageobject.nav.CollapsibleNavObject`
"""

from .webpage import WebPageObject
from .nav import (
    NavLinkObject, NavMenuObject, NavObject, CollapsibleNavObject
)
from .form import FormObject, InputObject
from .modal import ModalObject

