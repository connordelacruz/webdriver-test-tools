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

    :param description: The desired description string

    :return: Validated description string with double quotes replaced with
        single quotes
    """
    # Replace double quotes with single quotes to avoid breaking the docstring
    validated_description = description.replace('"', "'")
    if validated_description != description:
        cmd.print_info('Replaced double quotes with single quotes in class description')
    return validated_description


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
    # Validate module_name (and append .py if not already present)
    module_name = cmd.validate_module_filename(module_name)
    # Validate class_name
    class_name = cmd.validate_class_name(class_name)
    # Validate description name (if present)
    if description is not None:
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

