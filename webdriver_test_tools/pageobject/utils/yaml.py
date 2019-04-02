from selenium.webdriver.common.by import By
import yaml


# TODO: move some more generic functions to webdriver_test_tools.common?


# General YAML Utilities

# TODO: error handling?
# TODO: convert ints to strings? (e.g. for numeric keys)
def parse_yaml_file(path):
    """Parses a YAML file and returns a dictionary representation of it

    :param path: Path to the YAML file

    :return: A dictionary representation of the YAML file
    """
    with open(path, 'r') as file:
        loaded = yaml.load(file, loader=yaml.FullLoader)
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
    # TODO: error handling when keys are missing or values are invalid
    locate_by_attr = locator_dict['by'].upper()
    locate_by = getattr(By, locate_by_attr, None)
    return (locate_by, locator_dict['locator'])

