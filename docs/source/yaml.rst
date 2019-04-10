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

   * ``form_locator``: `Locator dictionary <Locator Dictionaries>`_ for the
     ``<form>`` element
   * ``submit_locator``: `Locator dictionary <Locator Dictionaries>`_ for the
     form's submit button
   * ``inputs``: List of form `inputs <Inputs>`_

.. _yaml-inputs:

Inputs
~~~~~~

The items in the form ``inputs`` list have the following keys:

   * ``name``: **(Required)** The ``name`` attribute of the element. If the
     element doesn't have a name attribute, set this to any unique identifier
     (i.e. not used as the ``name`` value for another input in the form)
   * ``input_locator``: **(Required if element has no ``name`` attribute)**
     `Locator dictionary <Locator Dictionaries>`_ for the element. If provided,
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

   * ``modal_locator``: `Locator dictionary <Locator Dictionaries>`_ for the
     modal container element
   * ``close_locator``: `Locator dictionary <Locator Dictionaries>`_ for the
     modal close button


Example
-------

.. literalinclude:: ../example/yaml-example/modal.yml

