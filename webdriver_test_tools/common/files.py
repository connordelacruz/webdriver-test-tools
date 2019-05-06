"""Common functions for working with files and Jinja templates"""

import os
import re

import jinja2

# Exceptions

class FileUtilError(Exception):
    """Exception raised if utility functions fail"""
    pass

# File utility functions

def touch(filepath):
    """'Touch' a file. Creates an empty file if it doesn't exist, leaves existing files
    unchanged

    :param filepath: Path of the file to touch
    """
    open(filepath, 'a').close()


def create_directory(target_path, directory_name):
    """Creates a directory in the target path if it doesn't already exist

    :param target_path: The path to the directory that will contain the new one
    :param directory_name: The name of the directory to create in the target path

    :return: The path to the newly created (or already existing) directory
    """
    path = os.path.join(target_path, directory_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# Template utility functions

def render_template(template_path, context):
    """Returns the rendered contents of a jinja template

    :param template_path: The path to the jinja template
    :param context: Jinja context used to render template

    :return: Results of rendering jinja template
    """
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './'),
        trim_blocks=True, lstrip_blocks=True
    ).get_template(filename).render(context)


def render_template_to_file(template_path, context, target_path):
    """Writes rendered jinja template to a file

    :param template_path: The path to the jinja template
    :param context: Jinja context used to render template
    :param target_path: File path to write the rendered template to
    """
    with open(target_path, 'w') as f:
        file_contents = render_template(template_path, context)
        f.write(file_contents)


def create_file_from_template(template_path, target_path, filename, context,
                              target_filename=None, overwrite=True):
    """Short hand function that renders a template with the specified filename followed
    by a '.j2' extension from the template path to a file with the specified name in
    the target path

    The use of '.j2' as a file extension is to distinguish templates from package
    modules.

    :param template_path: Path to template directory
    :param target_path: Path to target directory
    :param filename: Name of the template file. Will be used as the filename for the
        rendered file written to the target directory
    :param context: Jinja context used to render template
    :param target_filename: (Optional) If specified, use a different filename
        for the created file. If not specified, will use the value of
        ``filename``
    :param overwrite: (Default: True) If False, a FileUtilError will be raised
        when a file with the same name and path already exists

    :return: The file path to the newly created file
    """
    if target_filename is None:
        target_filename = filename
    file_template = os.path.join(template_path, filename + '.j2')
    file_target = os.path.join(target_path, target_filename)
    if not overwrite and os.path.exists(file_target):
        message_format = 'File "{}" already exists'
        raise FileUtilError(message_format.format(file_target))
    render_template_to_file(file_template, context, file_target)
    return file_target


# Validation

def validate_filename(filename, allow_spaces=False):
    """Strips invalid characters from a filename

    Considers `POSIX "fully portable filenames"
    <http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282>`__
    valid. These include:

        A-Z a-z 0-9 ._-

    Filenames cannot begin with a hyphen.

    :param filename: The desired file name (without path)
    :param allow_spaces: (Default = False) If True, spaces will be considered
        valid characters

    :return: Filename with invalid characters removed
    """
    regex = r'^-|[^\d\w\. -]' if allow_spaces else r'^-|[^\d\w\.-]'
    return re.sub(regex, '', filename)