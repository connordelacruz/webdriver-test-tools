from abc import ABC, abstractmethod
from webdriver_test_tools.pageobject import utils, BasePage


class YAMLParsingPageObject(BasePage, ABC):
    """Abstract subclass of :class:`BasePage
    <webdriver_test_tools.pageobject.base.BasePage>` with the basic attributes
    and abstract method for parsing YAML representations of page objects.

    Since this subclasses :class:`BasePage
    <webdriver_test_tools.pageobject.base.BasePage>`, prototypes that implement
    this only need to subclass ``YAMLParsingPageObject``.

    Page object prototypes that implement this will need to set the following
    attribute:

    :var YAMLParsingPageObject._YAML_ROOT_KEY: String for the expected root key
        in the parsed YAML. Usually a descriptor of the prototype (e.g. 'form')

    The abstract method :meth:`parse_yaml` is partially implemented and returns
    the results of parsing the YAML file and retrieving the value at
    ``_YAML_ROOT_KEY``. Implementations of ``parse_yaml()`` can call
    ``super().parse_yaml(file_name)`` to get the dictionary, e.g.:

        .. code-block:: python

            def parse_yaml(self, file_name):
                parsed_yaml = super().parse_yaml(file_path)
                ...

    This class also includes the following attribute, which should be set in
    subclasses of the prototype classes that implement this:

    :var YAMLParsingPageObject.YAML_FILE: Path to a YAML file representing the
        page object. This file is parsed during initialization using
        :meth:`parse_yaml` (if it's set)
    """

    # TODO: abstract property?
    _YAML_ROOT_KEY = None

    YAML_FILE = None

    def __init__(self, driver):
        super().__init__(driver)
        if self.YAML_FILE:
            self.parse_yaml(self.YAML_FILE)
        elif hasattr(self, 'no_yaml_init') and callable(self.no_yaml_init):
            self.no_yaml_init()

    @abstractmethod
    def parse_yaml(self, file_path):
        """Partially implemented abstract method for parsing YAML
        representation of the page object. Implementations of this can call
        ``super().parse_yaml(file_path)`` to get the value of the parsed file
        at :attr:`_YAML_ROOT_KEY`

        :param file_path: Full path to the YAML file

        :return: Dictionary of parsed YAML at :attr:`_YAML_ROOT_KEY`
        """
        try:
            parsed_yaml = utils.yaml.parse_yaml_file(file_path)[self._YAML_ROOT_KEY]
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                "Missing top level '{}' key in YAML".format(self._YAML_ROOT_KEY)
            )
        return parsed_yaml

    def no_yaml_init(self):
        """Fallback method to call during ``__init__()`` if :attr:`YAML_FILE`
        is not set.

        Subclasses should implement this method if any part of the
        initialization process needs to be handled differently when
        :attr:`YAML_FILE` is not set.
        """
        pass

