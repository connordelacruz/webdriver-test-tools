"""Subclasses of BasePage with additional functions for convenience.

These classes define common operations and attributes for various common components.
These can be subclassed in test projects if useful.

Prototype Classes
=================

This module imports the following classes.

.. autoclass:: webdriver_test_tools.pageobject.webpage.WebPageObject
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.pageobject.nav.NavObject
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.pageobject.nav.CollapsibleNavObject
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.pageobject.form.FormObject
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.pageobject.modal.ModalObject
    :members:
    :undoc-members:
    :noindex:

"""

from .webpage import WebPageObject
from .nav import NavObject, CollapsibleNavObject
from .form import FormObject
from .modal import ModalObject

