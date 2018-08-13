"""Functions for common command line formatting and procedures.

:var cmd.INDENT: Constant for terminal indentation
:var cmd.COLORS: Color/formatting functions for different types of output
"""

import re
import os
from blessings import Terminal

# Formatting

_term = Terminal()

# Prepend to input prompts
PROMPT_PREFIX = '> '
INDENT = ' ' * 3

COLORS = {
    None: str,
    'error': _term.bold_red,
    'warning': _term.yellow,
    'success': _term.green,
    'prompt': _term.magenta,
    'title': _term.blue,
    'emphasize': _term.bold,
}


# Printing

def print_exception(e):
    """Format and print the string representation of an exception

    :param e: The exception to print
    """
    print(COLORS['error'](str(e)))


def print_validation_warning(text):
    """Format and print a warning message when user input was modified in a prompt validation function

    :param text: Warning message to print. Should indicate what was changed to make user input valid
    """
    print(COLORS['warning'](text))


# User Input

class ValidationError(Exception):
    """Exception raised if input validation fails"""
    pass


def validate_nonempty(text):
    """Input validation function. Raises ValidationError if text is empty

    :param text: Text to validate

    :return: Validated text
    """
    if not text:
        raise ValidationError('Please enter some text.')
    return text


def validate_yn(answer):
    """Validate y/n prompts

    :param answer: User response to y/n prompt

    :return: True if user answered yes, False if user answered no
    """
    answer = answer.lower().strip()
    if answer not in ['y', 'yes', 'n', 'no']:
        raise ValidationError('Please enter "y" or "n".')
    return answer in ['y', 'yes']


def validate_package_name(package_name):
    """Removes and replaces characters to ensure a string is a valid python package name

    :param package_name: The desired package name

    :return: Modified package_name with whitespaces and hyphens replaced with
        underscores and all invalid characters removed
    """
    # Trim outer whitespace and replace inner whitespace and hyphens with underscore
    validated_package_name = re.sub(r'\s+|-+', '_', package_name.strip())
    # Remove non-alphanumeric or _ characters
    validated_package_name = re.sub(r'[^\w\s]', '', validated_package_name)
    # Remove leading characters until we hit a letter or underscore
    validated_package_name = re.sub(r'^[^a-zA-Z_]+', '', validated_package_name)
    if not validated_package_name:
        raise ValidationError('Please enter a valid package name.')
    # Alert user of any changes made in validation
    if package_name != validated_package_name:
        message_format = 'Name was changed to {} in order to be a valid python package'
        print_validation_warning(message_format.format(validated_package_name))
    return validated_package_name


# TODO: ensure duplicate validation_warnings don't appear
def validate_module_filename(module_filename):
    """Removes and replaces characters to ensure a string is a valid python
    module file name

    :param module_filename: The desired module file name. If the .py extension
        is excluded, it will be appended after validation

    :return: Modified module_filename with whitespaces and hyphens replaced with
        underscores, all invalid characters removed, and a '.py' extension
        appended (if necessary)
    """
    # Strip .py extension if present
    validated_module_filename, ext = os.path.splitext(module_filename.strip())
    try:
        # Python packages an modules have the same naming conventions
        validated_module_filename = validate_package_name(validated_module_filename)
    except ValidationError as e:
        raise ValidationError('Please enter a valid module name.')
    # Append .py extension
    validated_module_filename += '.py'
    # Alert the user of any changes made in validation
    if module_filename != validated_module_filename:
        message_format = 'Name was changed to {} in order to be a valid python module file'
        print_validation_warning(message_format.format(validated_module_filename))
    return validated_module_filename


# TODO: ensure duplicate validation_warnings don't appear
def validate_class_name(class_name):
    """Removes and replaces characters to ensure a string is a valid python
    class name

    :param class_name: The desired classname

    :return: Modified class_name with invalid characters removed/replaced
    """
    # TODO: Validate differently than packages?
    try:
        validated_class_name = validate_package_name(class_name)
    except ValidationError as e:
        raise ValidationError('Please enter a valid class name.')
    # Alert the user of any changes made in validation
    if class_name != validated_class_name:
        message_format = 'Name was changed to {} in order to be a valid python class name'
        print_validation_warning(message_format.format(validated_class_name))
    # Print warning if first letter isn't capital
    # (python is forgiving about class names but convention says it should be camel case)
    if validated_class_name[0] != validated_class_name[0].upper():
        print_validation_warning('Warning: Class name should start with a capital letter')
    return validated_class_name


def prompt(text, *description, default=None, validate=validate_nonempty, trailing_newline=True):
    """Prompt the user for input and validate it

    :param text: Text to display in prompt
    :param description: (Optional) Positional arguments after text will be printed once before user is prompted for
        input. Each argument will be printed on a new line
    :param default: (Optional) default value
    :param validate: (Default = validate_nonempty) Validation function for input
    :param trailing_newline: (Default = True) Print a blank line after receiving user
        input and successfully validating

    :return: Validated input
    """
    if description:
        print(*description, sep='\n')
    prompt_text = '{} [{}]: '.format(text, default) if default is not None else text + ': '
    prompt_text = COLORS['prompt'](PROMPT_PREFIX + prompt_text)
    while True:
        val = input(prompt_text).strip()
        if default is not None and not val:
            val = default
        try:
            val = validate(val)
        except ValidationError as e:
            print_exception(e)
            continue
        break
    if trailing_newline:
        print('')
    return val

