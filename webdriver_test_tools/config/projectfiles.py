
class ProjectFilesConfig:
    """Configurations for generated project files

    :var ENABLE_PAGE_OBJECT_YAML: If True, new page objects using a supported
        prototype will be generated with YAML parsing by default, unless the
        ``--no-yaml`` flag is specified. If False, ``new page`` will always
        generate python-only page objects regardless of YAML support, unless
        the ``--yaml`` flag is specified when using a supported prototype
    """
    # TODO: add template

    # TODO: re-phrase doc to be more helpful?
    ENABLE_PAGE_OBJECT_YAML = True

