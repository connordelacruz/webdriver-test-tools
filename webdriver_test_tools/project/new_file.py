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

#: Maps prototype names to the base name of the corresponding template files
#: and a list of file extensions for each file.
#: Empty string maps to generic BasePage template
PAGE_OBJECT_TEMPLATE_MAP = {
    '': {
        'name': 'base_page',
        'types': ['py']
    },
    FORM_PROTOTYPE: {
        'name' : 'form_object',
        'types': ['py', 'yml']
    },
    MODAL_PROTOTYPE: {
        'name' : 'modal_object',
        'types': ['py', 'yml']
    },
    NAV_PROTOTYPE: {
        'name' : 'nav_object',
        'types': ['py', 'yml']
    },
    COLLAPSIBLE_NAV_PROTOTYPE: {
        'name' : 'collapsible_nav_object',
        'types': ['py', 'yml']
    },
    WEB_PAGE_PROTOTYPE: {
        'name' : 'web_page_object',
        'types': ['py', 'yml']
    },
}

#: List of valid prototype names
PROTOTYPE_NAMES = [
    prototype for prototype in PAGE_OBJECT_TEMPLATE_MAP
    if prototype != ''
]

#: List of prototype names that support YAML parsing
YAML_PROTOTYPE_NAMES = [
    prototype for prototype, options in PAGE_OBJECT_TEMPLATE_MAP.items()
    if 'yml' in options.get('types', [])
]

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
    :param module_name: Python module name to use when creating the new file
        (without the .py extension, as this name is used when creating any
        additional non-Python files)
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

    :return: List of paths for each new file created
    """
    context = {
        'test_package': test_package,
        'module_name': module_name,
        'class_name': class_name,
        'description': description,
    }
    if file_type == PAGE_TYPE:
        return _new_page(test_package_path, context,
                         prototype=kwargs.get('prototype', ''),
                         use_yaml=kwargs.get('use_yaml', True),
                         overwrite=force)
    else:
        return _new_test(test_package_path, context,
                         overwrite=force)


def _new_page(test_package_path, context,
              prototype='', use_yaml=True, overwrite=False):
    """Create a new page object file

    :param test_package_path: The root directory of the test package
    :param context: Jinja context to use when creating the file. Assumes
        ``context`` has the 'module_name' key set
    :param prototype: (Default: '') Key in :data:`PAGE_OBJECT_TEMPLATE_MAP`
        specifying the prototype template to use. Defaults to empty string
        (generic page object)
    :param use_yaml: (Default: True) If True, generate .py and .yml files for
        supported prototypes. If False, just generate .py files. Templates will
        render different attributes based on this setting
    :param overwrite: (Default: False) If True, force overwrite if attempting
        to create a file that already exists

    :return: List of paths for each new file created
    """
    template_path = os.path.join(TEMPLATE_PATH, TEMPLATE_MAP[PAGE_TYPE])
    target_path = os.path.join(test_package_path, DIRECTORY_MAP[PAGE_TYPE])
    # Get info on template(s) for prototype
    template_map = PAGE_OBJECT_TEMPLATE_MAP[prototype]
    # Add 'use_yaml' to context
    context['use_yaml'] = use_yaml
    # If not using YAML, exclude .yml templates
    file_types = [
        ext for ext in template_map['types']
        if use_yaml or ext != 'yml'
    ]
    # Keep track of files created
    new_files = []
    for ext in file_types:
        template_filename = '{}.{}'.format(template_map['name'], ext)
        target_filename = '{}.{}'.format(context['module_name'], ext)
        new_files.append(create_file_from_template(
            template_path, target_path, template_filename, context,
            target_filename=target_filename, overwrite=overwrite
        ))
    return new_files


def _new_test(test_package_path, context, overwrite=False):
    """Create a new test file

    :param test_package_path: The root directory of the test package
    :param context: Jinja context to use when creating the file. Assumes
        ``context`` has the 'module_name' key set
    :param overwrite: (Default: False) If True, force overwrite if attempting
        to create a file that already exists

    :return: List of paths for each new file created
    """
    target_path = os.path.join(test_package_path, DIRECTORY_MAP[TEST_TYPE])
    template_filename = TEMPLATE_MAP[TEST_TYPE]
    target_filename = context['module_name'] + '.py'
    new_file = create_file_from_template(
        TEMPLATE_PATH, target_path, template_filename, context,
        target_filename=target_filename, overwrite=overwrite
    )
    # Return a list to keep value consistent with _new_page()
    return [new_file]



