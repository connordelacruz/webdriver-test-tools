"""Version information about the package

:var __version__: The version number for the package
:var __devstatus__: PyPI classifier for current development status on the project
:var __selenium__: The version of the selenium package used when developing/testing this
    package.
"""

__version__ = '0.30.0'
__devstatus__ = 'Development Status :: 2 - Pre-Alpha'
__selenium__ = '3.11.0'


def get_version_info():
    """Returns a dictionary with version information about the webdriver_test_tools package

    :return: Dictionary with keys 'version', 'devstatus', and 'selenium'
    """
    return {
        'version': __version__,
        'devstatus': __devstatus__,
        'selenium': __selenium__,
    }
