"""Wrapper functions for scroll module. Gives deprecation warning now that the
functions have moved and calls the new function name
"""

from . import scroll
import warnings


def _deprecation_warning(function_name):
    new_name = function_name.replace('scroll_', 'scroll.', 1)
    msg = 'actions.{}() deprecated, use actions.{}() instead.'.format(function_name, new_name)
    warnings.warn(msg, DeprecationWarning)


def scroll_into_view(driver, element, align_to_top=True):
    _deprecation_warning('scroll_into_view')
    scroll.into_view(driver, element, align_to_top)


def scroll_to_and_click(driver, element, align_to_top=True):
    _deprecation_warning('scroll_to_and_click')
    scroll.to_and_click(driver, element, align_to_top)


def scroll_to_position(driver, x, y):
    _deprecation_warning('scroll_to_position')
    scroll.to_position(driver, x, y)


def scroll_to_element(driver, element, offset=0, align_to_top=True):
    _deprecation_warning('scroll_to_element')
    scroll.to_element(driver, element, offset, align_to_top)


def scroll_into_view_fixed_nav(driver, target_element, fixed_element, additional_offset=0, align_to_top=True):
    _deprecation_warning('scroll_into_view_fixed_nav')
    scroll.into_view_fixed_nav(driver, target_element, fixed_element, additional_offset, align_to_top)


