from webdriver_test_tools.config import projectfiles


class ProjectFilesConfig(projectfiles.ProjectFilesConfig):
    """Configurations for generated project files"""

    # Page Object Configurations

    # The default YAML parsing setting to use when creating page objects with
    # the ``new page`` command.
    # If True, generate .py and .yml files for supported prototype by default
    # unless the ``--no-yaml`` flag is specified.
    # If False, just generate .py files for all prototypes unless the
    # ``--yaml`` flag is specified.
    ENABLE_PAGE_OBJECT_YAML = True
