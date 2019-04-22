
class ProjectFilesConfig:
    """Configurations for generated project files

    :var ENABLE_PAGE_OBJECT_YAML: The default YAML parsing setting to use when
        creating page objects with the ``new page``. If True, generate .py and
        .yml files for supported prototype by default unless the ``--no-yaml``
        flag is specified. If False, just generate .py files for all prototypes
        unless the ``--yaml`` flag is specified.
    """
    ENABLE_PAGE_OBJECT_YAML = True

