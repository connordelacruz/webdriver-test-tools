"""Functions for common command line formatting and procedures.

:var cmd.INDENT: Constant for terminal indentation
:var cmd.COLORS: Color/formatting functions for different types of output
"""

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

