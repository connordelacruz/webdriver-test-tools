"""Wrapper functions for form module. Gives deprecation warning now that the
actions module will not import * from forms in the future and to use
actions.form.<function> instead
"""

from . import form
import warnings


def _deprecation_warning(function_name):
    fmt = 'actions.{0}() is deprecated and may be removed in the future. use actions.form.{0}() instead.'
    warnings.warn(fmt.format(function_name), DeprecationWarning)


def fill_form_inputs(driver, form_element, input_name_map):
    _deprecation_warning('fill_form_inputs')
    form.fill_form_inputs(driver, form_element, input_name_map)


def fill_form_input(driver, form_element, name, value):
    _deprecation_warning('fill_form_input')
    form.fill_form_input(driver, form_element, name, value)


