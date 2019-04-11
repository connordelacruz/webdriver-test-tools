# TODO: import, document
from abc import ABC, abstractmethod
import os
from webdriver_test_tools.pageobject import utils, BasePage


class YAMLParsingPageObject(BasePage, ABC):
    # TODO: doc

    # TODO: abstract property?
    YAML_FILE = None
    YAML_ROOT_KEY = None

    def __init__(self, driver):
        super().__init__(driver)
        if self.YAML_FILE:
            self.parse_yaml(self.YAML_FILE)

    @abstractmethod
    def parse_yaml(self, file_path):
        # TODO: doc
        try:
            parsed_yaml = utils.yaml.parse_yaml_file(file_path)[self.YAML_ROOT_KEY]
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                "Missing top level '{}' key in YAML".format(self.YAML_ROOT_KEY)
            )
        return parsed_yaml

