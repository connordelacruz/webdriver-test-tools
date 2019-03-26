"""Functions for creating a new test/page module."""

from webdriver_test_tools.common.files import *
from webdriver_test_tools.project import templates

# TODO: organize module

# New file types
TEST_TYPE = 'test'
PAGE_TYPE = 'page'

TEMPLATE_PATH = templates.templates.get_path()

# TODO: figure out how prototype templates factor in
#: Maps file type to corresponding template file
TEMPLATE_MAP = {
    TEST_TYPE: 'test_case.py',
    # TODO: find a cleaner way of doing this?
    PAGE_TYPE: 'page_object/base_page.py',
}

# Prototype names
FORM_PROTOTYPE = 'form'

PROTOTYPE_NAMES = [
    FORM_PROTOTYPE,
]

# TODO: doc and implement
PAGE_OBJECT_TEMPLATE_MAP = {
    '': 'base_page.py',
    'form': 'form_object.py',
    # TODO:
}

#: Maps file type to corresponding subdirectory in a test package
DIRECTORY_MAP = {
    TEST_TYPE: 'tests',
    PAGE_TYPE: 'pages',
}


# TODO: implement **kwargs and update docstring
def new_file(test_package_path, test_package, file_type, module_name, class_name,
             description=None, force=False, **kwargs):
    """Create a new project file

    This method assumes parameters have been validated. :func:`main()
    <webdriver_test_tools.project.new_file.main()>` handles input validation
    before calling this function

    :param test_package_path: The root directory of the test package
    :param test_package: The python package name of the test package
    :param file_type: The type of file to create. Valid file types are stored
        as global variables with the _TYPE suffix
    :param module_name: Filename to use for the new python module
    :param class_name: Name to use for the initial test class
    :param description: (Optional) Description to use in the docstring of the initial class
    :param force: (Default: False) If True, force overwrite if a file with the
        same name already exists

    :return: Path of the new file
    """
    # TODO: re-work for new setup
    template_file = TEMPLATE_MAP[file_type]
    target_path = os.path.join(test_package_path, DIRECTORY_MAP[file_type])
    # TODO: TESTING
    if kwargs and 'prototype' in kwargs:
        print('Prototype:',kwargs['prototype'])
    # TODO: does context need to be different for prototypes?
    context = {
        'test_package': test_package,
        'module_name': module_name,
        'class_name': class_name,
        'description': description,
    }
    return create_file_from_template(
        TEMPLATE_PATH, target_path, template_file, context,
        target_filename=module_name, overwrite=force
    )
