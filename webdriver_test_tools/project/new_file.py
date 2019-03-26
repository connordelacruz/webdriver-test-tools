"""Functions for creating a new test/page module."""

from webdriver_test_tools.common.files import *
from webdriver_test_tools.project import templates

# TODO: organize module

# New file types
TEST_TYPE = 'test'
PAGE_TYPE = 'page'

TEMPLATE_PATH = templates.templates.get_path()

#: Maps file type to corresponding template file
TEMPLATE_MAP = {
    TEST_TYPE: 'test_case.py',
    # TODO: find a cleaner way of doing this?
    PAGE_TYPE: 'page_object/',
}

# Prototype names
FORM_PROTOTYPE = 'form'
MODAL_PROTOTYPE = 'modal'

PROTOTYPE_NAMES = [
    FORM_PROTOTYPE,
    MODAL_PROTOTYPE,
]

# TODO: doc and implement
PAGE_OBJECT_TEMPLATE_MAP = {
    '': 'base_page.py',
    FORM_PROTOTYPE: 'form_object.py',
    MODAL_PROTOTYPE: 'modal_object.py',
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
    template_file = TEMPLATE_MAP[file_type]
    # If this is a page, determine which template in page_object/ to use
    if file_type == PAGE_TYPE:
        # Default to empty string (base_page.py)
        prototype = kwargs.get('prototype', '')
        template_file = os.path.join(
            template_file, PAGE_OBJECT_TEMPLATE_MAP[prototype]
        )
    target_path = os.path.join(test_package_path, DIRECTORY_MAP[file_type])
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
