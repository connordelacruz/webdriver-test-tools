import warnings

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from webdriver_test_tools.pageobject import utils, BasePage, YAMLParsingPageObject
from webdriver_test_tools.webdriver import actions


# Link Page Objects

class NavLinkObject(BasePage):
    """Page object prototype for nav links"""

    class ActionTypes:
        """Link click/hover action types"""
        PAGE = 'page'
        SECTION = 'section'
        MENU = 'menu'
        NONE = 'none'
        # Click/hover support for each type
        CLICK_ACTIONS = [
            PAGE, SECTION, MENU, NONE
        ]
        HOVER_ACTIONS = [
            MENU, NONE
        ]
        # Required attributes for types
        REQUIRES_TARGET = [
            PAGE, SECTION
        ]

    def __init__(self, driver, link_dict, site_config):
        """Initialize ``NavLinkObject`` using parsed YAML or link dictionary

        See :ref:`YAML links documentation <yaml-links>` for details on
        ``link_dict`` syntax

        :param driver: Selenium WebDriver object
        :param link_dict: Link dictionary using syntax specified in :ref:`YAML
            links documentation <yaml-links>`. Must have 'name' and
            'link_locator' keys set
        :param site_config: Test project's :class:`SiteConfig` class. Used to
            determine any relative URLs specified in the 'target'

        :raises ValueError: if any of the keys in ``link_dict`` are set to
            invalid values
        :raises KeyError: if any of the required keys in ``link_dict`` are
            missing
        """
        super().__init__(driver)
        # 'name' and 'link_locator' required, so assume that they're valid keys
        # and raise errors otherwise
        self.name = link_dict['name']
        self.locator = utils.yaml.parse_locator_dict(link_dict['link_locator'])
        self.click_action = link_dict.get('click', self.ActionTypes.PAGE)
        if self.click_action not in self.ActionTypes.CLICK_ACTIONS:
            error_msg = "Invalid value 'click' action for link (link: {}). ".format(str(link_dict))
            error_msg += 'Valid click actions: {}'.format(str(self.ActionTypes.CLICK_ACTIONS))
            raise ValueError(error_msg)
        if self.click_action == self.ActionTypes.NONE:
            self.click_action = None
            # Click target should also be None
            self.target = None
        self.hover_action = link_dict.get('hover', None)
        if self.hover_action and self.hover_action not in self.ActionTypes.HOVER_ACTIONS:
            error_msg = "Invalid value 'hover' action for link (link: {}). ".format(str(link_dict))
            error_msg += 'Valid hover actions: {}'.format(str(self.ActionTypes.HOVER_ACTIONS))
            raise ValueError(error_msg)
        if self.hover_action == self.ActionTypes.NONE:
            self.hover_action = None
        # Get target attribute if required
        if self.click_action in self.ActionTypes.REQUIRES_TARGET:
            target = link_dict['target']
            # Add '#' to the front of section targets if not present
            if self.click_action == self.ActionTypes.SECTION and not target.startswith('#'):
                target = '#' + target
            if isinstance(target, dict):
                target = site_config.parse_relative_url_dict(target)
            self.target = target
        # Parse menu if applicable
        if self.ActionTypes.MENU in [self.click_action, self.hover_action]:
            self.menu = NavMenuObject(self.driver, link_dict['menu'], site_config)

    # WebElement retrieval

    def find_link_element(self):
        """Returns the ``WebElement`` object located by ``self.locator``

        Shorthand for ``self.find_element(self.locator)``

        :return: ``WebElement`` object for the link
        """
        return self.find_element(self.locator)

    # Actions

    def click_link(self):
        """Click the link

        :return: Return value depends on ``self.click_action``:

            * 'page': Returns the URL to the link target
            * 'section': Returns the target section ID (prefixed with '#')
            * 'menu': Returns a :class:`NavMenuObject` instance
            * None: Returns ``None``
        """
        actions.scroll.to_and_click(self.driver, self.find_link_element(), False)
        return self.menu if self.click_action == self.ActionTypes.MENU else self.target

    def hover_over_link(self):
        """Hover over the link element

        :return: :class:`NavMenuObject` instance (or ``None`` if no hover
            action is defined)
        """
        link_element = self.find_link_element()
        actions.scroll.into_view(self.driver, link_element, False)
        action_chain = ActionChains(self.driver)
        action_chain.move_to_element(link_element).perform()
        return self.menu if self.hover_action == self.ActionTypes.MENU else None


# Menu Page Objects

class NavMenuObject(BasePage):
    """Page object prototype for dropdown/collapsible nav menus"""

    def __init__(self, driver, menu_dict, site_config):
        """Initialize ``NavMenuObject`` using parsed YAML or the 'menu' key in
        a link dictionary

        See :ref:`YAML nav menus documentation <yaml-nav-menus>` for details on
        ``menu_dict`` syntax

        :param driver: Selenium WebDriver object
        :param menu_dict: Nav menu dictionary using syntax specified in
            :ref:`YAML nav menus documentation <yaml-nav-menus>`. Must have
            'menu_locator' and 'links' keys set
        :param site_config: Test project's :class:`SiteConfig` class. Used when
            initializing :class:`NavLinkObject` instances to determine any
            relative URLs specified in the 'target'

        :raises ValueError: if any of the keys in ``menu_dict`` are set to
            invalid values or if 2+ items in 'links' list have the same 'name'
        :raises KeyError: if any of the required keys in ``menu_dict`` are
            missing
        """
        super().__init__(driver)
        # 'menu_locator' is required, so assume it's a valid key and raise
        # errors otherwise
        self.locator = utils.yaml.parse_locator_dict(menu_dict['menu_locator'])
        self.links = {}
        for link_dict in menu_dict['links']:
            # TODO: except key error, update message to show menu?
            link_name = link_dict['name']
            if link_name in self.links:
                error_msg = "Multiple links with the same 'name' value in menu (name: {}). ".format(link_name)
                error_msg += 'link names must be unique'
                raise ValueError(error_msg)
            self.links[link_name] = NavLinkObject(self.driver, link_dict, site_config)

    # WebElement retrieval

    def find_menu_element(self):
        """Returns the ``WebElement`` object located by ``self.locator``

        Shorthand for ``self.find_element(self.locator)``

        :return: ``WebElement`` object for the menu
        """
        return self.find_element(self.locator)

    # Actions

    def click_link(self, link_name):
        """Click a link in the menu

        :param link_name: Name of the link (specified in YAML or link
            dictionary) i.e. a valid key in ``self.links``

        :return: The returned value of clicking the link. See
            :meth:`NavLinkObject.click_link` for possible values

        :raises KeyError: If ``link_name`` is not a valid key in ``self.links``
        """
        return self.links[link_name].click_link()

    def hover_over_link(self, link_name):
        """Hover over a link in the menu

        :param link_name: Name of the link (specified in YAML or link
            dictionary) i.e. a valid key in ``self.links``

        :return: The returned value of hovering over the link. See
            :meth:`NavLinkObject.hover_over_link` for possible values

        :raises KeyError: If ``link_name`` is not a valid key in ``self.links``
        """
        return self.links[link_name].hover_over_link()

    def is_visible(self):
        """Check if the menu element is visible

        :return: True if the element is displayed, False if not
        """
        try:
            visible = self.find_menu_element().is_displayed()
        except NoSuchElementException:
            visible = False
        return visible


# Navbar Page Objects

class NavObject(YAMLParsingPageObject):
    """Page object prototype for navbars

    Subclasses should set the following attributes:

    :var NavObject.YAML_FILE: Path to a YAML file representing the navbar
    :var NavObject.SITE_CONFIG: Test project's :class:`SiteConfig` class.
        Used for :class:`NavLinkObject` instances to determine any relative
        URLs specified for link targets

    The following attributes are determined based on the contents of
    :attr:`YAML_FILE` (or should be set in subclasses if :attr:`YAML_FILE` is
    ``None``):

    :var NavObject.FIXED: (Default: True) True if element is a fixed navbar,
        False otherwise. If set to False in a subclass,
        :meth:`click_page_link()` and :meth:`hover_over_page_link()` will
        scroll the target link into view before interacting with it
    :var NavObject.COLLAPSIBLE: (Default: False) True if the navbar is
        collapsible (e.g. for hamburger menus). If set to True,
        :attr:`MENU_LOCATOR`, :attr:`EXPAND_BUTTON_LOCATOR`, and (optionally)
        :attr:`COLLAPSE_BUTTON_LOCATOR` should also be set

    For collapsible navs, these additional attributes should also be specified
    in :attr:`YAML_FILE` (or should be set in subclasses if :attr:`YAML_FILE`
    is ``None``):

    :var NavObject.MENU_LOCATOR: (Required for collapsible) Locator for the
        collapsible menu element
    :var NavObject.EXPAND_BUTTON_LOCATOR: (Required for collapsible) Locator
        for the button that expands the nav menu
    :var NavObject.COLLAPSE_BUTTON_LOCATOR: (Optional) Locator for the button
        that collapses the nav menu. If unspecified, this will be set to the
        same value as :attr:`EXPAND_BUTTON_LOCATOR`

    The following attribute is set based on the 'links' key parsed from
    :attr:`YAML_FILE` (or parsed from :attr:`LINK_DICTS`, which should be set
    in subclasses if :attr:`YAML_FILE` is ``None``):

    :var NavObject.links: A dictionary mapping link names to the corresponding
        :class:`NavLinkObject` instances. The keys correspond with the ``name``
        keys in the YAML representation of the navbar (or the 'name' keys in
        :attr:`LINK_DICTS` if :attr:`YAML_FILE` is ``None``)

    If :attr:`YAML_FILE` is ``None``, subclasses must set the following
    attribute:

    :var NavObject.LINK_DICTS: List of link dictionaries. These are used to
        initialize the :class:`NavLinkObject` instances in :attr:`links` at
        runtime. These dictionaries use the same syntax as :ref:`YAML links
        <yaml-links>`

        .. todo::

            ``LINK_DICTS`` syntax is kind of cluttered, will likely re-work to
            be cleaner in future versions

    ---

    The following attributes are deprecated as of version 2.9.0, and will be
    removed in future versions:

    :var NavObject.LINK_MAP: Maps link text to a tuple containing its locator
        and the page object class for the target page, modal, section, etc (or
        None if need be). Override in subclasses

        .. deprecated:: 2.9.0
            :attr:`links` should be used instead

    :var NavObject.HOVER_MAP: Maps link text to a tuple containing its locator
        and the page object class for the menu, dropdown, etc that should
        appear on hover (or None if need be). Override in subclasses

        .. deprecated:: 2.9.0
            :attr:`links` should be used instead
    """

    _YAML_ROOT_KEY = 'nav'

    SITE_CONFIG = None

    # General nav attributes
    FIXED = True
    # Collapsible attributes
    COLLAPSIBLE = False
    MENU_LOCATOR = None
    COLLAPSE_BUTTON_LOCATOR = None
    EXPAND_BUTTON_LOCATOR = None

    # Link objects
    LINK_DICTS = []
    links = {}

    # Link maps
    LINK_MAP = {}
    HOVER_MAP = {}

    # Initialization

    def parse_yaml(self, file_path):
        """Parse a YAML representation of the nav object and set attributes
        accordingly

        See :ref:`YAML NavObjects doc <yaml-nav-objects>` for details on
        syntax.

        :param file_path: Full path to the YAML file
        """
        parsed_yaml = super().parse_yaml(file_path)
        self.FIXED = parsed_yaml.get('fixed', True)
        # Only retrieve if attribute is present (allows deprecated
        # CollapsibleNavObject to override default)
        if 'collapsible' in parsed_yaml:
            self.COLLAPSIBLE = parsed_yaml['collapsible']
        # Collapsible nav configurations
        if self.COLLAPSIBLE:
            try:
                self.MENU_LOCATOR = utils.yaml.parse_locator_dict(parsed_yaml['menu_locator'])
                self.EXPAND_BUTTON_LOCATOR = utils.yaml.parse_locator_dict(parsed_yaml['expand_button_locator'])
                if 'collapse_button_locator' in parsed_yaml:
                    self.COLLAPSE_BUTTON_LOCATOR = utils.yaml.parse_locator_dict(parsed_yaml['collapse_button_locator'])
                else:
                    self.COLLAPSE_BUTTON_LOCATOR = self.EXPAND_BUTTON_LOCATOR
            except KeyError as e:
                error_msg = 'Missing required {} key in collapsible nav YAML. '.format(e)
                error_msg += "If 'collapsible' is set to true, 'expand_button_locator' and 'menu_locator' must also be set"
                raise utils.yaml.YAMLKeyError(error_msg)
        self._initialize_links(parsed_yaml['links'])

    def no_yaml_init(self):
        """Initialize ``self.links`` using values in :attr:`LINK_DICTS`"""
        if self.COLLAPSIBLE:
            if not self.COLLAPSE_BUTTON_LOCATOR:
                self.COLLAPSE_BUTTON_LOCATOR = self.EXPAND_BUTTON_LOCATOR
        self._initialize_links(self.LINK_DICTS, from_yaml=False)

    def _initialize_links(self, link_dicts, from_yaml=True):
        """Initialize :class:`NavLinkObject` instances in ``self.links``

        :param link_dicts: List of link dictionaries
        :param from_yaml: (Default: True) Whether or not this was parsed from
            YAML. Exceptions raised will be different based on this
        """
        # TODO: verify and document exceptions
        self.links = {}
        for link_dict in link_dicts:
            try:
                link_name = link_dict['name']
                # Link names must be unique
                if link_name in self.links:
                    error_msg = "Multiple links with the same 'name' value (name: {}). ".format(link_name)
                    error_msg += 'link names must be unique'
                    raise utils.yaml.YAMLValueError(error_msg) if from_yaml else ValueError(error_msg)
                # Initialize NavLinkObject
                self.links[link_name] = NavLinkObject(self.driver, link_dict, self.SITE_CONFIG)
            except KeyError as e:
                if from_yaml:
                    error_message = 'Missing required {} key in link YAML (link: {})'.format(e, str(link_dict))
                    raise utils.yaml.YAMLKeyError(error_message)
                # Preserve stack trace for key error if not parsing YAML
                else:
                    raise
            except ValueError as e:
                # Raise YAML error if applicable
                if from_yaml:
                    raise utils.yaml.YAMLKeyError(error_msg)
                # Preserve stack trace for key error if not parsing YAML
                else:
                    raise

    # Nav Actions

    def click_link(self, link_name):
        """Click a link on the navbar

        :param link_name: Name of the link (specified in YAML or link
            dictionary) i.e. a valid key in ``self.links``

        :return: The returned value of clicking the link. See
            :meth:`NavLinkObject.click_link` for possible values

        :raises KeyError: If ``link_name`` is not a valid key in ``self.links``
        """
        return self.links[link_name].click_link()

    def hover_over_link(self, link_name):
        """Hover over a link in the navbar

        :param link_name: Name of the link (specified in YAML or link
            dictionary) i.e. a valid key in ``self.links``

        :return: The returned value of hovering over the link. See
            :meth:`NavLinkObject.hover_over_link` for possible values

        :raises KeyError: If ``link_name`` is not a valid key in ``self.links``
        """
        return self.links[link_name].hover_over_link()

    # Collapsible Nav Actions

    def click_expand_button(self):
        """Click the button to expand the nav menu

        .. note::

            For collapsible navs only. If :attr:`COLLAPSIBLE` is ``False``, a
            warning will be raised and the method will return
        """
        if not self.COLLAPSIBLE:
            warnings.warn(
                'NavObject.click_expand_button() called on a non-collapsible NavObject, method will not be executed'
            )
            return
        button = self.find_element(self.EXPAND_BUTTON_LOCATOR)
        if not self.FIXED:
            actions.scroll.into_view(self.driver, button)
        button.click()

    def click_collapse_button(self):
        """Click the button to collapse the nav menu

        .. note::

            For collapsible navs only. If :attr:`COLLAPSIBLE` is ``False``, a
            warning will be raised and the method will return
        """
        if not self.COLLAPSIBLE:
            warnings.warn(
                'NavObject.click_collapse_button() called on a non-collapsible NavObject, method will not be executed'
            )
            return
        button = self.find_element(self.COLLAPSE_BUTTON_LOCATOR)
        if not self.FIXED:
            actions.scroll.into_view(self.driver, button)
        button.click()

    def is_expanded(self):
        """Check if the nav menu is expanded

        .. note::

            For collapsible navs only. If :attr:`COLLAPSIBLE` is ``False``, a
            warning will be raised and the method will return

        This method checks if the element located by :attr:`MENU_LOCATOR`
        exists and is visible. This should be sufficient for many common
        implementations of collapsible navs, but can be overridden if this
        isn't a reliable detection method for an implementation

        :return: True if the nav menu is expanded, False if it's collapsed
        """
        if not self.COLLAPSIBLE:
            warnings.warn(
                'NavObject.is_expanded() called on a non-collapsible NavObject, method will not be executed'
            )
            return
        try:
            expanded = self.find_element(self.MENU_LOCATOR).is_displayed()
        except NoSuchElementException:
            expanded = False
        return expanded

    # Deprecated Methods

    def click_page_link(self, link_map_key):
        """
        .. deprecated:: 2.9.0
            Use :meth:`click_link` instead

        Click one of the page links and return a page object class for the link
        target

        :param link_map_key: Key into :attr:`LINK_MAP` for the link to click on

        :return: Corresponding page object class for the link target (if applicable)
        """
        warnings.warn(
            'NavObject.click_page_link() is deprecated and may be removed in future versions, use click_link() instead',
            DeprecationWarning
        )
        if link_map_key in self.LINK_MAP:
            link_tuple = self.LINK_MAP[link_map_key]
            link = self.find_element(link_tuple[0])
            if not self.FIXED:
                actions.scroll.into_view(self.driver, link)
            link.click()
            # Initialize the target page object and return it
            return None if link_tuple[1] is None else link_tuple[1](self.driver)

    def hover_over_page_link(self, link_map_key):
        """
        .. deprecated:: 2.9.0
            Use :meth:`hover_over_link` instead

        Hover mouse over one of the page links

        :param link_map_key: Key into :attr:`HOVER_MAP` for the link to hover mouse over

        :return: Corresponding page object class for the hover dropdown/container/etc
            (if applicable)
        """
        warnings.warn(
            'NavObject.hover_over_page_link() is deprecated and may be removed in future versions, use hover_over_link() instead',
            DeprecationWarning
        )
        if link_map_key in self.HOVER_MAP:
            link_tuple = self.HOVER_MAP[link_map_key]
            link = self.find_element(link_tuple[0])
            if not self.FIXED:
                actions.scroll.into_view(self.driver, link)
            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(link).perform()
            # Initialize the target page object and return it
            return None if link_tuple[1] is None else link_tuple[1](self.driver)


class CollapsibleNavObject(NavObject):
    """
    .. deprecated:: 2.9.0
        Use :class:`NavObject` with ``COLLAPSIBLE = True`` instead

    Subclass of :class:`NavObject` with additional methods for collapsible nav
    menus

    In addition to the variables for :class:`NavObject`, the following
    variables need to be defined for collapsible navs

    :var CollapsibleNavObject.EXPAND_BUTTON_LOCATOR: Locator for the button
        that expands the nav menu
    :var CollapsibleNavObject.COLLAPSE_BUTTON_LOCATOR: Locator for the button
        that expands the nav menu
    :var CollapsibleNavObject.MENU_CONTAINER_LOCATOR: Locator for the
        collapsing/expanding container of the navigation menu
    """

    COLLAPSIBLE = True
    # Deprecated
    MENU_CONTAINER_LOCATOR = None

    def __init__(self, driver):
        warnings.warn(
            'CollapsibleNavObject is deprecated, use NavObject with COLLAPSIBLE set to True instead',
            DeprecationWarning
        )
        super().__init__(driver)
        # Set MENU_LOCATOR to match deprecated attribute if specified
        if self.MENU_CONTAINER_LOCATOR:
            self.MENU_LOCATOR = self.MENU_CONTAINER_LOCATOR

