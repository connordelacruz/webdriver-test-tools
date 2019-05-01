===============================
Page Object Prototypes Overview
===============================

.. contents::

Overview
========

.. todo expand

The ``webdriver_test_tools`` package includes pre-defined subclasses of
:class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>` for common
components like forms and navbars. These classes define common methods and
attributes to reduce the amount of code needed to create page objects.

Prototype classes support simplified YAML representations as well as pure
Python. For details on YAML syntax, see :doc:`yaml`.


FormObject
==========

The :class:`FormObject <webdriver_test_tools.pageobject.form.FormObject>`
prototype is used to represent forms, their inputs, and their submit button.

Attributes
----------

``FormObject`` subclasses define the following attributes:

   * ``FORM_LOCATOR``: WebDriver locator tuple for the form element
   * ``SUBMIT_LOCATOR``: WebDriver locator tuple for the submit button

``FormObject`` subclasses may also have the following optional attribute:

   * ``SUBMIT_SUCCESS_CLASS``: Page object class representing the page/modal/etc
     that is expected to appear on successful submission

``FormObject`` subclasses will have the following attributes at runtime. These
are populated based on the contents of ``YAML_FILE`` or ``INPUT_DICT``:

   * ``inputs``: A dictionary mapping input names to the corresponding
     :class:`InputObject <webdriver_test_tools.pageobject.form.InputObject>`
     instances


Methods
-------

* :meth:`FormObject.fill_inputs
  <webdriver_test_tools.pageobject.form.FormObject.fill_inputs>`: Fill form
  inputs
* :meth:`FormObject.get_input_values
  <webdriver_test_tools.pageobject.form.FormObject.get_input_values>`: Get the
  current values of form inputs
* :meth:`FormObject.submit_is_enabled
  <webdriver_test_tools.pageobject.form.FormObject.submit_is_enabled>`: Checks
  if the submit button is enabled
* :meth:`FormObject.click_submit
  <webdriver_test_tools.pageobject.form.FormObject.click_submit>`: Click the
  submit button


ModalObject
===========

The :class:`ModalObject <webdriver_test_tools.pageobject.modal.ModalObject>`
prototype is used to represent modals, their body content, and their close
button.

Attributes
----------

``ModalObject`` subclasses define the following attributes:

   * ``MODAL_LOCATOR``: WebDriver locator tuple for the modal element
   * ``CLOSE_LOCATOR``: WebDriver locator tuple for the modal close button

``ModalObject`` subclasses may also have the following optional attribute:

   * ``MODAL_BODY_CLASS``: Page object class representing the contents of the
     modal body


Methods
-------

* :meth:`ModalObject.is_displayed
  <webdriver_test_tools.pageobject.modal.ModalObject.is_displayed>`: Checks if
  the modal is currently visible
* :meth:`ModalObject.click_close_button
  <webdriver_test_tools.pageobject.modal.ModalObject.click_close_button>`: Click
  the modal's close button
* :meth:`ModalObject.get_modal_body
  <webdriver_test_tools.pageobject.modal.ModalObject.get_modal_body>`: Returns
  an instance of the class defined in ``MODAL_BODY_CLASS`` (or ``None`` if not
  set)


NavObject
=========

The :class:`NavObject <webdriver_test_tools.pageobject.nav.NavObject>` prototype
is used to represent navbars.

Attributes
----------

``NavObject`` subclasses may define the following optional attributes:

   * ``FIXED``: (Default: ``True``) True if the navbar is fixed to the window
   * ``COLLAPSIBLE``: (Default: ``False``) True if the navbar is collapsible
     (e.g. uses a hamburger menu)

If ``COLLAPSIBLE`` is set to ``True``, subclasses should define the following
attributes:

   * ``MENU_LOCATOR``: Locator for the collapsible menu element
   * ``EXPAND_BUTTON_LOCATOR``: Locator for the button that expands the nav menu
   * ``COLLAPSE_BUTTON_LOCATOR``: (Optional) Locator for the button that
     collapses the nav menu. Leave unset if this is the same as
     ``EXPAND_BUTTON_LOCATOR``

``NavObject`` subclasses will have the following attributes at runtime. These
are populated based on the contents of ``YAML_FILE`` or ``LINK_DICTS``:

   * ``links``: A dictionary mapping link names to the corresponding
     :class:`NavLinkObject <webdriver_test_tools.pageobject.nav.NavLinkObject>`
     instances


Methods
-------

All ``NavObject`` subclasses have the following methods:

   * :meth:`NavObject.click_link
     <webdriver_test_tools.pageobject.nav.NavObject.click_link>`: Click a link
     in the navbar
   * :meth:`NavObject.hover_over_link
     <webdriver_test_tools.pageobject.nav.NavObject.hover_over_link>`: Hover
     over a link in the navbar

Collapsible ``NavObject`` subclasses have additional methods:

   * :meth:`NavObject.click_expand_button
     <webdriver_test_tools.pageobject.nav.NavObject.click_expand_button>`: Click
     the button to expand the nav menu
   * :meth:`NavObject.click_collapse_button
     <webdriver_test_tools.pageobject.nav.NavObject.click_collapse_button>`:
     Click the button to collapse the nav menu
   * :meth:`NavObject.is_expanded
     <webdriver_test_tools.pageobject.nav.NavObject.is_expanded>`: Check if the
     nav menu is expanded


WebPageObject
=============

.. todo re-phrase? move to top since it's the simplest example? explain other
.. todo usages (e.g. methods to get page object representations of items on that page)

The :class:`WebPageObject
<webdriver_test_tools.pageobject.webpage.WebPageObject>` prototype is used to
represent entire pages.

Attributes
----------

``WebPageObject`` subclasses define the following attribute:

   * ``PAGE_URL``: Full URL to the page

``WebPageObject`` subclasses may also have the following optional attribute:

   * ``PAGE_FILENAME``: Filename of the page (or path relative to a base URL
     configured in a project's :class:`SiteConfig
     <webdriver_test_tools.config.site.SiteConfig>`)


Methods
-------

* :meth:`WebPageObject.get_page_title
  <webdriver_test_tools.pageobject.webpage.WebPageObject.get_page_title>`:
  Returns the title of the current page

