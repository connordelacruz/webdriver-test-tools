"""Functions for common command line formatting and procedures.

:var cmd.INDENT: Constant for terminal indentation
:var cmd.COLORS: Color/formatting functions for different types of output
"""
# TODO: rename to something less confusing than cmd.cmd

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
    'info': _term.cyan,
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


def print_warning(text):
    """Format and print a warning message

    :param text: Warning message to print
    """
    print(COLORS['warning'](text))


def print_info(text):
    """Format and print info message

    :param text: Info message to print
    """
    print(COLORS['info'](text))


# User Input

class ValidationError(Exception):
    """Exception raised if input validation fails"""
    pass


def print_validation_change(message_format, original, changed):
    """Inform the user of changes to their input during validation.
    Used to keep output format consistent

    :param message_format: A format string with 2 positional fields, one for
        the original value and one for the altered value. These fields should
        be surrounded with double quotes for better readability.

        example:

            '"{0}" changed to "{1}" for compatibility'

    :param original: The original user input
    :param changed: The input after being altered
    """
    print_info(message_format.format(original, changed))


def validate_nonempty(text):
    """Input validation function. Raises ValidationError if text is empty

    :param text: Text to validate

    :return: Validated text
    """
    if not text:
        raise ValidationError('Please enter some text.')
    return text


# TODO: rename to avoid confusion?
def validate_choice(choices, shorthand_choices={}, error_msg=None):
    """Returns a validation function for input with specific choice options

    :param choices: A list of **lowercase** strings the user can choose from
    :param shorthand_choices: (Optional) A dictionary mapping short hand
        answers to options in ``choices``. If user answers prompt with one of
        the keys in ``shorthand_choices``, the validation function will treat
        their answer as ``shorthand_choices[answer]``.

        The following example values would allow 'y' and 'n' to be accepted as
        'yes' and 'no', respectively:

            .. code-block:: python

                choices = ['yes', 'no']
                shorthand_choices = {
                    'y': 'yes',
                    'n': 'no',
                }
                validate_yes_no = validate_choice(choices, shorthand_choices)
                # Both of the following return 'yes'
                result0 = validate_yes_no('yes')
                result1 = validate_yes_no('y')

    :param error_msg: (Optional) Custom validation error message. By default,
        validation errors will have the message:

            ``'Please select a valid choice: [<choices>]'``

        where ``<choices>`` is a comma separated representation of the values
        in ``choices``.

    :return: A validation function that accepts a string and returns the
        corresponding item from ``choices`` if the string is valid
    """
    if error_msg is None:
        error_msg = 'Please select a valid choice: [{}]'.format(', '.join(choices))
    def val(answer):
        answer = answer.lower().strip()
        if answer in shorthand_choices:
            answer = shorthand_choices[answer]
        if answer not in choices:
            raise ValidationError(error_msg)
        return answer
    return val


def validate_yn(answer):
    """Validate y/n prompts

    :param answer: User response to y/n prompt. If a boolean value is passed
        (e.g. if a prompt received parsed_input=True), it is treated as a y/n
        answer and considered valid input

    :return: True if user answered yes, False if user answered no
    """
    # If a boolean value was passed, return it
    if isinstance(answer, bool):
        return answer
    answer = answer.lower().strip()
    if answer not in ['y', 'yes', 'n', 'no']:
        raise ValidationError('Please enter "y" or "n".')
    return answer in ['y', 'yes']


def _validate_python_identifier(identifier):
    """Removes and replaces characters and returns a valid python identifier

    Python identifiers include letters, numbers, and underscores and cannot
    begin with a number

    :param identifier: The desired identifier string

    :return: Modified identifier with invalid characters removed or replaced
    """
    # Trim outer whitespace and replace inner whitespace and hyphens with underscore
    validated_identifier = re.sub(r'\s+|-+', '_', identifier.strip())
    # Remove non-alphanumeric or _ characters
    validated_identifier = re.sub(r'[^\w\s]', '', validated_identifier)
    # Remove leading characters until we hit a letter or underscore
    validated_identifier = re.sub(r'^[^a-zA-Z_]+', '', validated_identifier)
    if not validated_identifier:
        raise ValidationError('Please enter a valid python identifier.')
    return validated_identifier


def validate_package_name(package_name):
    """Removes and replaces characters to ensure a string is a valid python package name

    :param package_name: The desired package name

    :return: Modified package_name with whitespaces and hyphens replaced with
        underscores and all invalid characters removed
    """
    try:
        validated_package_name = _validate_python_identifier(package_name)
    except ValidationError as e:
        raise ValidationError('Please enter a valid package name.')
    # Alert user of any changes made in validation
    if package_name != validated_package_name:
        print_validation_change(
            '"{0}" was changed to "{1}" in order to be a valid python package',
            package_name, validated_package_name
        )
    return validated_package_name


def validate_module_name(module_name):
    """Removes and replaces characters to ensure a string is a valid python
    module file name

    :param module_name: The desired module name. If the name ends in .py, the
        extension will be removed

    :return: Modified module_name with whitespaces and hyphens replaced with
        underscores and all invalid characters removed
    """
    # Strip .py extension if present
    module_name, ext = os.path.splitext(module_name.strip())
    try:
        validated_module_name = _validate_python_identifier(module_name)
    except ValidationError as e:
        raise ValidationError('Please enter a valid module name.')
    # Alert the user of any changes made in validation
    if module_name != validated_module_name:
        print_validation_change(
            '"{0}" was changed to "{1}" in order to be a valid python module file',
            module_name, validated_module_name
        )
    return validated_module_name


def validate_module_filename(module_filename, suppress_ext_change=True):
    """Removes and replaces characters to ensure a string is a valid python
    module file name

    Essentially a wrapper around :func:`validate_module_name` that makes sure a
    .py extension is added to the end if needed

    :param module_filename: The desired module file name. If the .py extension
        is excluded, it will be appended after validation
    :param suppress_ext_change: (Default: True) If False, print message when
        appending .py extension to file name. Suppressed by default, as the
        user shouldn't typically be required to append .py themselves

    :return: Modified module_filename with whitespaces and hyphens replaced with
        underscores, all invalid characters removed, and a '.py' extension
        appended (if necessary)
    """
    # Strip .py extension if present
    module_name, ext = os.path.splitext(module_filename.strip())
    validated_module_name = validate_module_name(module_name)
    # Append .py extension
    validated_module_filename = validated_module_name + '.py'
    if ext != '.py' and not suppress_ext_change:
        print_info('Added .py extension for filename')
    return validated_module_filename


def validate_class_name(class_name):
    """Removes and replaces characters to ensure a string is a valid python
    class name

    :param class_name: The desired class name

    :return: Modified class_name with invalid characters removed/replaced
    """
    # TODO: Validate differently than packages? (e.g. 'class name' -> 'ClassName'?)
    try:
        validated_class_name = _validate_python_identifier(class_name)
    except ValidationError as e:
        raise ValidationError('Please enter a valid class name.')
    # Alert the user of any changes made in validation
    if class_name != validated_class_name:
        print_validation_change(
            '"{0}" was changed to "{1}" in order to be a valid python class name',
            class_name, validated_class_name
        )
    # Print warning if first letter isn't capital
    # (python is forgiving about class names but convention says it should be camel case)
    if validated_class_name[0] != validated_class_name[0].upper():
        print_warning('Warning: Class name should start with a capital letter')
    return validated_class_name


def prompt(text, *description, default=None, validate=validate_nonempty,
           parsed_input=None, trailing_newline=True):
    """Prompt the user for input and validate it

    :param text: Text to display in prompt
    :param description: (Optional) Positional arguments after text will be printed once before user is prompted for
        input. Each argument will be printed on a new line
    :param default: (Optional) default value
    :param validate: (Default = validate_nonempty) Validation function for input
    :param parsed_input: (Default = None) If ``parsed_input`` is set to
        something other than ``None``, parser will attempt to validate it. If
        validation is successful, the input prompt will be skipped and the
        validated value of ``parsed_input`` will be returned. This allows for
        input to be passed through command line arguments, but still prompt the
        user in the event that it can't be validated
    :param trailing_newline: (Default = True) Print a blank line after receiving user
        input and successfully validating

    :return: Validated input
    """
    # Attempt to bypass prompt if parsed_input is not None
    if parsed_input is not None:
        try:
            val = validate(parsed_input)
        except ValidationError as e:
            print_exception(e)
        else:
            # If no errors were raised, return validated input
            return val
    # Input prompt
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

