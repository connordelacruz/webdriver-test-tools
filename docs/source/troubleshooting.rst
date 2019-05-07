=====================
Troubleshooting Tests
=====================

.. contents::

.. todo doc overview

.. todo Issue reporting if it's something with the framework?

Common Issues
=============

"Element is not clickable at point (x,y). Other element would receive the click"
--------------------------------------------------------------------------------

.. currentmodule:: webdriver_test_tools.webdriver.actions

.. todo Flesh out example? Explore other potential solutions?

You may run across errors saying **"Element is not clickable at point (x,y).
Other element would receive the click: <element>"**. This is often due to a
fixed element obstructing the element you're attempting to click, such as a
sticky navbar or violator.

The :mod:`webdriver.actions.scroll
<webdriver_test_tools.webdriver.actions.scroll>` submodule includes the
:func:`scroll.into_view_fixed_nav` function, which scrolls an element into view
relative to a fixed object that may obstruct it. For example, suppose we want to
click on ``button_element``, but it's obstructed by a fixed navbar
``nav_element``:

.. code-block:: python

   ...
   # Scroll element to the top of the screen, relative to the fixed nav
   scroll.into_view_fixed_nav(driver, button_element, nav_element)
   # Click the button 
   button_element.click()

Despite the name, this function is not limited to objects fixed to the top of
the screen. Setting the optional parameter ``align_to_top=False`` will scroll
the target element into view relative to a fixed element on the bottom of the
screen. E.g. suppose we want to click on ``button_element``, but it's obstructed
by ``violator_element`` which is fixed to the bottom of the screen:

.. code-block:: python

   ...
   # Scroll element to the bottom of the screen, relative to the violator
   scroll.into_view_fixed_nav(driver, button_element, violator_element,
                              align_to_top=False)
   # Click the button 
   button_element.click()

For more information, see the API documentation for
:func:`scroll.into_view_fixed_nav`.


Accounting for timeouts on slow sites or pages
----------------------------------------------

.. todo Accounting for slow pages


Issues with specific browsers
-----------------------------

.. todo Specific browser drivers


Tools for Troubleshooting
=========================

.. todo Screenshots, input() pausing


