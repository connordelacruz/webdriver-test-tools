"""Functions for creating a new test/page module."""

from webdriver_test_tools import cmd
from webdriver_test_tools.common.files import *
from webdriver_test_tools.project import templates


TEST_TYPE = 'test'
PAGE_TYPE = 'page'

TEMPLATE_PATH = templates.templates.get_path()
#: Maps file type to corresponding template file
TEMPLATE_MAP = {
    TEST_TYPE: 'test_case.py',
    PAGE_TYPE: 'page_object.py',
}
#: Maps file type to corresponding subdirectory in a test package
DIRECTORY_MAP = {
    TEST_TYPE: 'tests',
    PAGE_TYPE: 'pages',
}


# TODO: convert to cmd.validate_choice?
def validate_file_type(file_type):
    """Validate file type and return the corresponding template filename and
    target directory

    :param file_type: The string to validate

    :return: ``(template_file, target_dir)`` where ``template_file`` is the
        corresponding filename for the template and ``target_dir`` is the
        corresponding directory where the new file should be placed
    """
    file_type = file_type.lower().strip()
    if file_type not in TEMPLATE_MAP:
        raise cmd.ValidationError('File type "{}" invalid'.format(file_type))
    template_file = TEMPLATE_MAP[file_type]
    target_dir = DIRECTORY_MAP[file_type]
    return template_file, target_dir


def validate_description(description):
    """Replaces double quotes with single quotes in class description

    If the description is ``None`` or an empty string, this function considers
    it valid and returns ``None``

    :param description: The desired description string

    :return: Validated description string with double quotes replaced with
        single quotes or ``None`` if the description is empty
    """
    if description is None or description == '':
        return None
    # Replace double quotes with single quotes to avoid breaking the docstring
    validated_description = description.replace('"', "'")
    if validated_description != description:
        cmd.print_info('Replaced double quotes with single quotes in class description')
    return validated_description


# Main methods

def new_file(test_package_path, test_package, file_type, module_name, class_name,
             description=None, force=False):
    """Create a new project file

    :param test_package_path: The root directory of the test package
    :param test_package: The python package name of the test package
    :param file_type: The type of file to create. Valid file types are stored
        as global variables with the _TYPE suffix
    :param module_name: Filename to use for the new python module
    :param class_name: Name to use for the initial test class
    :param description: (Optional) Description to use in the docstring of the initial class
    :param force: (Default: False) If True, force overwrite if a file with the
        same name already exists
    """
    template_file, target_dir = validate_file_type(file_type)
    target_path = os.path.join(test_package_path, target_dir)
    # TODO: use main() as entry point, assume any input will be validated before new_file() call
    # Validate module_name (and append .py if not already present)
    module_name = cmd.validate_module_filename(module_name)
    # Validate class_name
    class_name = cmd.validate_class_name(class_name)
    # Validate description name (None is considered valid)
    description = validate_description(description)
    context = {
        'test_package': test_package,
        'module_name': module_name,
        'class_name': class_name,
        'description': description,
    }
    new_file_path = create_file_from_template(
        TEMPLATE_PATH, target_path, template_file, context,
        target_filename=module_name, overwrite=force
    )
    # Output new file path on success
    print(cmd.COLORS['success']('\nFile created.'))
    print(new_file_path)


# TODO: main function for prompts?

def main(test_package_path, test_package,
         file_type=None, module_name=None, class_name=None,
         description=None, force=False):
    """Command line dialogs for creating a new file

    This method accepts optional arguments for each of its prompts. If these
    are set to something other than ``None``, their corresponding input prompts
    will be skipped unless validation for that parameter fails.

    ``file_type``, ``module_name``, and ``class_name`` are the 3 values
    required to create a new file. If these are all set to something other than
    ``None``, this method will default to an empty ``description`` unless one
    is provided.

    ``force`` is the only optional parameter that does not have a prompt. It
    will default to ``False`` unless the ``--force`` flag is used when calling
    this method.

    :param test_package_path: The root directory of the test package
    :param test_package: The python package name of the test package
    :param file_type: (Optional) The type of file to create. If valid, the user
        won't be prompted for input and this will be used instead. Valid file
        types are stored as global variables with the _TYPE suffix
    :param module_name: (Optional) Filename to use for the new python module.
        If valid, the user won't be prompted for input and this will be used
        instead
    :param class_name: (Optional) Name to use for the initial test class.
        If valid, the user won't be prompted for input and this will be used
        instead
    :param description: (Optional) Description to use in the docstring of the
        initial class. User will only be prompted for a description if one or
        more of the positional arguments (``file_type``, ``module_name``, and
        ``class_name``) are set to ``None``
    :param force: (Default: False) If True, force overwrite if a file with the
        same name already exists
    """
    # TODO: add Ctrl + C handling from initialize.main()?
    # if module_name and class_name are set, use defaults for description and force
    if module_name and class_name and description is None:
        description = ''
    _validate_file_type = cmd.validate_choice(
        ['test','page'], shorthand_choices={'t': 'test', 'p': 'page'}
    )
    validated_file_type = cmd.prompt(
        '[t]est/[p]age',
        'Create a new test case or page object?',
        validate=_validate_file_type,
        parsed_input=file_type
    )
    validated_module_name = cmd.prompt(
        'Module file name',
        'Enter a file name for the new {} module'.format(validated_file_type),
        validate=cmd.validate_module_filename,
        parsed_input=module_name
    )
    class_type = 'test case' if validated_file_type == 'test' else 'page object'
    validated_class_name = cmd.prompt(
        '{} class name'.format(class_type.capitalize()),
        'Enter a name for the initial {} class'.format(class_type),
        validate=cmd.validate_class_name,
        parsed_input=class_name
    )
    validated_description = cmd.prompt(
        'Description',
        '(Optional) Enter description of the new {} class'.format(class_type),
        validate=validate_description,
        default='',
        parsed_input=description
    )

    new_file(
        test_package_path, test_package,
        file_type=validated_file_type, module_name=validated_module_name,
        class_name=validated_class_name, description=validated_description,
        force=force
    )


