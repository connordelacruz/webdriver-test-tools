
class ProjectFilesConfig:
    # TODO: doc, add template
    # TODO: make sure this is compatible with old projects that don't have this config

    # TODO: move to docstring, correct if anything changes
    # If True, new page objects using a supported prototype will be generated
    # with YAML parsing by default, unless the --no-yaml flag is specified. If
    # False, `new page` will always generate python-only page objects
    # regardless of YAML support, unless the --yaml flag is specified when
    # using a supported prototype
    ENABLE_PAGE_OBJECT_YAML = True

