======================
Page Object YAML files
======================

.. contents::

.. todo overview, list supported classes, link to YAML syntax doc, expand on general syntax?

General Syntax
==============

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

