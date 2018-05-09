"""Version information about the package

:var __version__: The version number for the package
:var __devstatus__: PyPI classifier for current development status on the project
:var __selenium__: The version of the selenium package used when developing/testing this
    package.
"""
from .__about__ import __version__, __devstatus__, __selenium__


def get_version_info():
    """Returns a dictionary with version information about the webdriver_test_tools package

    :return: Dictionary with keys 'version', 'devstatus', and 'selenium'
    """
    return {
        'version': __version__,
        'devstatus': __devstatus__,
        'selenium': __selenium__,
    }
