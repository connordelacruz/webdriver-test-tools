"""Utilities for parsing YAML page object representations."""
from selenium.webdriver.common.by import By
import yaml


# Exceptions

class YAMLParseException(Exception):
    """Generic exception for parsing YAML files"""
    pass

class YAMLKeyError(YAMLParseException):
    """Missing key in parsed YAML"""
    pass

class YAMLValueError(YAMLParseException):
    """Invalid value in parsed YAML"""
    pass

# General YAML Utilities

def parse_yaml_file(path):
    """Parses a YAML file and returns a dictionary representation of it

    :param path: Path to the YAML file

    :return: A dictionary representation of the YAML file
    """
    with open(path, 'r') as file:
        loaded = yaml.load(file, Loader=yaml.FullLoader)
    return loaded


# WebDriver YAML constructs

# TODO: better name (refactor usages)
def to_locator(locator_dict):
    """Takes a locator dictionary from a parsed YAML file and returns the
    locator tuple

    :param locator_dict: Locator dictionary from a parsed YAML file. A valid
        locator dict must have the following keys:

            * 'by': name of attribute from selenium.webdriver.common.by.By
            * 'locator': locator string

        .. note::

            The string mapped to the 'by' key will be capitalized before
            checking if it's a valid attribute of the ``By`` class

    :return: Parsed WebDriver locator tuple
    """
    try:
        locate_by_attr = locator_dict['by'].upper()
        locate_by = getattr(By, locate_by_attr)
        return (locate_by, locator_dict['locator'])
    except KeyError as e:
        error_msg = 'Missing required {0} key in locator YAML (locator: {1})'.format(
            e, str(locator_dict)
        )
        raise YAMLKeyError(error_msg)
    except AttributeError as e:
        error_msg = "Invalid 'locate_by' value (locate_by: {}). ".format(locate_by_attr)
        error_msg += 'Must be a valid attribute of selenium.webdriver.common.by.By'
        raise YAMLValueError(error_msg)

