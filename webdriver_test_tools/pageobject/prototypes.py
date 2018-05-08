"""Subclasses of BasePage with additional functions for convenience.

These classes define common operations and attributes for various common components.
These can be subclassed in test projects if useful.
"""

from .webpage import WebPageObject
from .nav import NavObject, CollapsibleNavObject
from .form import FormObject
from .modal import ModalObject

