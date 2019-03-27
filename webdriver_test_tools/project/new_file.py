"""Functions for creating a new test/page module."""

from webdriver_test_tools.common.files import *
from webdriver_test_tools.project import templates


# New file types
TEST_TYPE = 'test'
PAGE_TYPE = 'page'

TEMPLATE_PATH = templates.templates.get_path()

#: Maps file type to corresponding template file/directory relative to the
#: template path
TEMPLATE_MAP = {
    TEST_TYPE: 'test_case.py',
    PAGE_TYPE: 'page_object/',
}

# Prototype names
FORM_PROTOTYPE = 'form'
MODAL_PROTOTYPE = 'modal'
NAV_PROTOTYPE = 'nav'
COLLAPSIBLE_NAV_PROTOTYPE = 'collapsible nav'
WEB_PAGE_PROTOTYPE = 'web page'

#: List of valid prototype names
PROTOTYPE_NAMES = [
    FORM_PROTOTYPE,
    MODAL_PROTOTYPE,
    NAV_PROTOTYPE,
    COLLAPSIBLE_NAV_PROTOTYPE,
    WEB_PAGE_PROTOTYPE,
]

#: Maps prototype names to corresponding template file name.
#: Empty string maps to generic BasePage template
PAGE_OBJECT_TEMPLATE_MAP = {
    '': 'base_page.py',
    FORM_PROTOTYPE: 'form_object.py',
    MODAL_PROTOTYPE: 'modal_object.py',
    NAV_PROTOTYPE: 'nav_object.py',
    COLLAPSIBLE_NAV_PROTOTYPE: 'collapsible_nav_object.py',
    WEB_PAGE_PROTOTYPE: 'web_page_object.py',
}

#: Maps file type to corresponding subdirectory in a test package
DIRECTORY_MAP = {
    TEST_TYPE: 'tests',
    PAGE_TYPE: 'pages',
}


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
    :param description: (Optional) Description to use in the docstring of the
        initial class
    :param force: (Default: False) If True, force overwrite if a file with the
        same name already exists

    This method accepts additional keyword arguments for type-specific
    arguments.

    Page kwargs:

        * ``prototype``: Key in :data:`PAGE_OBJECT_TEMPLATE_MAP` specifying the
          prototype template to use. Defaults to empty string (generic page
          object)

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

