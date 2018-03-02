# Functions for commonly repeated driver actions

# Imports
# ----------------------------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# Driver Actions
# ----------------------------------------------------------------

# Scrolling
# --------------------------------

def scroll_into_view(driver, element, align_to_top=True):
    """Scroll to an element

    :param driver: Selenium webdriver object
    :param element: Element to scroll to
    :param align_to_top: (Default = True) Aligns element to top of scrollable parent if True, aligns it to the bottom if False
    """
    script_string = 'arguments[0].scrollIntoView({});'.format(str(align_to_top).lower())
    driver.execute_script(script_string, element)

def scroll_to_position(driver, x, y):
    """Scroll window to the specified x,y coordinates

    Executes JavaScript window.scroll(x,y)

    :param driver: Selenium WebDriver object
    :param x: Horizontal scroll coordinate
    :param y: Vertical scroll coordinate
    """
    script_string = 'window.scroll({},{});'.format(x,y)
    driver.execute_script(script_string)

def scroll_to_element(driver, element, offset=0, align_to_top=True):
    """Vertically scroll to an element with an optional offset

    When align_to_top=True, the scroll y coordinate is calculated:
        element.offsetTop - offset
    When align_to_top=False, the scroll y coordinate is calculated:
        element.offsetTop + element.offsetHeight - window.innerHeight + offset

    :param driver: Selenium WebDriver object
    :param element: WebElement object for the target element
    :param offset: (Default = 0) Scroll offset
    :param align_to_top: (Default = True) Aligns element to the top of scrollable parent if True, aligns it to the bottom if False
    """
    scroll_y = int(element.get_property('offsetTop'))
    if align_to_top:
        scroll_y -= offset
    else:
        script_string = 'return window.innerHeight;'
        viewport_height = int(driver.execute_script(script_string))
        scroll_y += int(element.get_property('offsetHeight')) - viewport_height + offset
    scroll_to_position(driver, 0, scroll_y)

def scroll_into_view_fixed_nav(driver, target_element, fixed_element, additional_offset=0, align_to_top=True):
    """Scroll an element into view offset by the height of a fixed element so it's not obstructed

    :param driver: Selenium WebDriver object
    :param target_element: WebElement object for the target element
    :param fixed_element: WebElement object for the fixed nav
    :param additional_offset: (Default = 0) Additional offset from the top
    :param align_to_top: (Default = True) Aligns element to the top of scrollable parent if True, aligns it to the bottom if False
    """
    offset = int(fixed_element.get_property('offsetHeight')) + additional_offset
    scroll_to_element(driver, target_element, offset, align_to_top)


# Forms/Inputs
# --------------------------------

def fill_form_inputs(driver, form_element, input_name_map):
    """Takes a dictionary mapping input names to the desired values and fill out the form accordingly

    Iterates through input_name_map and calls fill_form_input() to handle filling in the input based on its type

    :param driver: Selenium webdriver object (largely for scrolling into view)
    :param form_element: The Selenium WebElement for the form or container with the desired inputs. Used for locating the input elements by name in case there are other elements on the page with the same name attribute
    :param input_name_map: A dictionary mapping the name of the input to the value to set it to. See the documentation for fill_form_input() for value types for the different inputs.
    """
    # Iterate through input_name_map
    for name, value in input_name_map.items():
        fill_form_input(driver, form_element, name, value)

def fill_form_input(driver, form_element, name, value):
    """Takes the name and value of a form input and determines what type it is to fill it appropriately.

    :param driver: Selenium webdriver object (largely for scrolling clickable inputs into view)
    :param form_element: The Selenium WebElement for the form or container with the desired inputs. Used for locating the input elements by name in case there are other elements on the page with the same name attribute
    :param name: The name attribute of the input
    :param value: The desired value to set the input to.
        For checkbox elements, this value should be a boolean (True=checked, False=unchecked).
        For radio elements, this should be the value attribute of the radio to select.
        For single select elements, this value should be the value of the option to select.
        For multiple select elements, this value should be a list of values of the options to select.
        For file inputs, this value should be a filepath to the desired file.
        For other input types (text, number, etc) this should be a string representation of the values to enter into it.
    """
    input_element = form_element.find_element_by_name(name)
    # If element tag isn't input, use tag name as input_type (e.g. select)
    input_type = input_element.tag_name if input_element.tag_name != 'input' else input_element.get_attribute('type')
    # figure out the input type, handle appropriately
    # Radio Buttons
    if input_type == 'radio':
        # Radio groups often have the same name and are identified by value,
        # so don't pass input_element in case it's not the right one
        select_radio_input(driver, form_element, name, value)
    # Checkboxes
    elif input_type == 'checkbox':
        toggle_checkbox_input(driver, input_element, value)
    # Selects
    elif input_type == 'select':
        # Use select_option() for single selects or selecting single option in multi selects
        if input_element.get_attribute('multiple') is None or not isinstance(value, list):
            select_option(input_element, value)
        # Use select_multiple_options() for multiple selects
        else:
            select_multiple_options(input_element, value)
    # Other input types (text, file, etc)
    else:
        fill_field_input(input_element, value)


def select_radio_input(driver, form_element, name, value):
    """Selects a radio input with the specified name and value attributes

    :param driver: Selenium webdriver object. Used for scrolling the element into view before clicking element
    :param form_element: The Selenium WebElement for the form or container with the desired inputs. Used for locating the input elements by name in case there are other elements on the page with the same name attribute
    :param name: Name attribute of the radio input(s)
    :param value: Value attribute of the radio input to select
    """
    radio_selector = 'input[type=radio][name={}][value={}]'.format(name,value)
    radio_element = form_element.find_element_by_css_selector(radio_selector)
    # Selenium throws an error when trying to click something out of view
    scroll_into_view(driver, radio_element, False)
    radio_element.click()

def toggle_checkbox_input(driver, checkbox_element, value):
    """Set the checked state of a checkbox input

    First checks if the checkbox value doesn't match the desired value. If not, it then checks if element is visible. If it is, scroll to it and click it. If it isn't, it tries to find a label for the element by getting the element id and selecting a label with that id as the for attribute. If it finds one, it scrolls to that and clicks it.

    :param driver: Selenium webdriver object. Used for scrolling the element into view before clicking element
    :param checkbox_element: WebElement for the checkbox to toggle
    :param value: True to ensure box is checked, False to ensure it's unchecked
    """
    if checkbox_element.is_selected() != value:
        # If checkbox is visible, scroll it into view and click
        if checkbox_element.is_displayed():
            # Selenium throws an error when trying to click something out of view
            scroll_into_view(driver, checkbox_element, False)
            checkbox_element.click()
        # Element might be invisible for styling. Try to find its label and click that
        else:
            checkbox_id = checkbox_element.get_attribute('id')
            label_css = 'label[for="{}"]'.format(checkbox_id)
            element_label = driver.find_element_by_css_selector(label_css)
            # Selenium throws an error when trying to click something out of view
            scroll_into_view(driver, element_label, False)
            element_label.click()

def fill_field_input(input_element, value, clear_current_value=False):
    """Fill an input that is normally typed into (e.g. inputs of type text, password, number, etc)

    :param input_element: WebElement for the input
    :param value: String of key presses to simulate using the send_keys() function
    :param clear_current_value: (Default = False) If True, clear out any existing value in the input before entering the new one
    """
    if clear_current_value:
        input_element.clear()
    input_element.send_keys(value)

def select_option(select_element, value):
    """Select an option in a select element

    :param select_element: WebElement for the select input
    :param value: Value of the option to select
    """
    select = Select(select_element)
    select.select_by_value(value)

def select_multiple_options(select_element, values, clear_current_selection=False):
    """Select options in a multiple select element

    :param select_element: WebElement for the select input
    :param values: List of values of the options to select
    :param clear_current_selection: (Default = False) If True, deselect all currently selected options before selection the new ones
    """
    select = Select(select_element)
    if clear_current_selection:
        select.deselect_all()
    for value in values:
        select.select_by_value(value)


