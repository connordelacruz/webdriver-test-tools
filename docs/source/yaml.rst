.. _yaml-page-objects:

======================
Page Object YAML files
======================

.. contents::

Overview
========

To simplify the process of creating new page objects, some page object prototype
classes support YAML representations of the object. Prototype classes that
support this will generate a ``.yml`` file in addition to a Python module when
using the ``new page --prototype <prototype>`` command.

The following sections detail YAML syntax specifically for
``webdriver_test_tools``. For a basic introduction to YAML syntax in general,
see `Ansible's YAML documentation`_.

.. _Ansible's YAML documentation: https://docs.ansible.com/ansible/2.7/reference_appendices/YAMLSyntax.html


Supported Prototype Classes
---------------------------

Currently, the following prototype classes support YAML parsing:  

   * :class:`FormObject <webdriver_test_tools.pageobject.form.FormObject>`
   * :class:`ModalObject <webdriver_test_tools.pageobject.modal.ModalObject>`
   * :class:`WebPageObject <webdriver_test_tools.pageobject.webpage.WebPageObject>`

YAML support will be added to more in future releases.

.. todo briefly go over YAML_FILE attribute


General Syntax
==============

This section documents the syntax of general page object constructs.

.. _yaml-locators:

Locator Dictionaries
--------------------

Element locators are represented by YAML dictionaries with the following
required keys:

   * ``by``: Locator strategy to use when finding the element. Use variable
     names of attributes in ``selenium.webdriver.common.by.By``:

      * ``CLASS_NAME``
      * ``CSS_SELECTOR``
      * ``ID``
      * ``LINK_TEXT``
      * ``NAME``
      * ``PARTIAL_LINK_TEXT``
      * ``TAG_NAME``
      * ``XPATH``

   * ``locator``: Value used to locate element with the specified locator
     strategy


.. _yaml-form-objects:

FormObjects
===========

:class:`FormObjects <webdriver_test_tools.pageobject.form.FormObject>` support
YAML representations of the form element using the following syntax.

Syntax
------

.. _yaml-forms:

Forms
~~~~~

Form objects have 3 required keys:

   * ``form_locator``: :ref:`Locator dictionary <yaml-locators>` for the
     ``<form>`` element
   * ``submit_locator``: :ref:`Locator dictionary <yaml-locators>` for the
     form's submit button
   * ``inputs``: List of form :ref:`inputs <yaml-inputs>`

.. _yaml-inputs:

Inputs
~~~~~~

The items in the form ``inputs`` list have the following keys:

   * ``name``: **(Required)** The ``name`` attribute of the element. If the
     element doesn't have a name attribute, set this to any unique identifier
     (i.e. not used as the ``name`` value for another input in the form)
   * ``input_locator``: **(Required if element has no ``name`` attribute)**
     :ref:`Locator dictionary <yaml-locators>` for the element. If provided,
     this will be used instead of ``name`` to find the element
   * ``type``: *(Default: ``text``)* The ``type`` attribute of the input
   * ``required``: *(Default: ``true``)* Whether or not the input is required to
     submit the form
   * ``options``: **(Required if ``type`` is ``radio``, ``select``, or a
     ``checkbox`` group (i.e. multiple checkboxes with the same name))** List of
     ``value`` attributes of radio inputs, select options, or checkboxes. A
     dictionary mapping values to labels is also valid (though only the map keys
     will be used, so the labels can be set to anything)


Example
-------

.. literalinclude:: ../example/yaml-example/form.yml


.. _yaml-modal-objects:

ModalObjects
============

:class:`ModalObjects <webdriver_test_tools.pageobject.modal.ModalObject>`
support YAML representations of the modal using the following syntax.

Syntax
------

Modal objects have 2 required keys:

   * ``modal_locator``: :ref:`Locator dictionary <yaml-locators>` for the modal
     container element
   * ``close_locator``: :ref:`Locator dictionary <yaml-locators>` for the modal
     close button


Example
-------

.. literalinclude:: ../example/yaml-example/modal.yml


.. _yaml-web-page-objects:

WebPageObjects
==============

:class:`WebPageObjects <webdriver_test_tools.pageobject.webpage.WebPageObject>`
support YAML representations of the modal using the following syntax.

Syntax
------

Web page objects have one required key ``url``, which can be set to either the
full URL to the page, or a dictionary containing the following keys:

   * ``path``: The path to the page, relative to the ``SiteConfig`` attribute
     specified in ``relative_to``
   * ``relative_to``: A valid attribute declared in the project's ``SiteConfig``
     class to use as a base URL. It is assumed that the value of this attribute
     has a trailing '/'

.. note::

   If 'url' is set to just the full URL to the page, the attribute
   ``PAGE_FILENAME`` will not be set in the ``WebPageObject``. If it is set to a
   dictionary, ``PAGE_FILENAME`` will be set to the value of 'path'


Example
-------

.. literalinclude:: ../example/yaml-example/web_page.yml


