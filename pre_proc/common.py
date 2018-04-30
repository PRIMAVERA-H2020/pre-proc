"""
common.py

Library code used by many functions.
"""
import inspect
import logging.config
import os
import subprocess

logger = logging.getLogger(__name__)


def run_command(command):
    """
    Run the command specified and return any output to stdout or stderr as
    a list of strings.
    :param str command: The complete command to run.
    :returns: Any output from the command as a list of strings.
    :raises RuntimeError: If the command did not complete successfully.
    """
    try:
        cmd_out = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                          shell=True)
    except subprocess.CalledProcessError as exc:
        msg = ('Command did not complete sucessfully.\ncommmand:\n{}\n'
               'produced error:\n{}'.format(command, exc.output))
        logger.warning(msg)
        raise RuntimeError(msg)

    if isinstance(cmd_out, str):
        return cmd_out.rstrip().split('\n')
    else:
        return None


def list_files(directory, suffix='.nc'):
    """
    Return a list of all the files with the specified suffix in the submission
    directory structure and sub-directories.

    :param str directory: The root directory of the submission
    :param str suffix: The suffix of the files of interest
    :returns: A list of absolute filepaths
    """
    nc_files = []

    dir_files = os.listdir(directory)
    for filename in dir_files:
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            nc_files.extend(list_files(file_path, suffix))
        elif file_path.endswith(suffix):
            nc_files.append(file_path)

    return nc_files


def ilist_files(directory, suffix='.nc'):
    """
    Return an iterator of all the files with the specified suffix in the
    submission directory structure and sub-directories.

    :param str directory: The root directory of the submission
    :param str suffix: The suffix of the files of interest
    :returns: A list of absolute filepaths
    """
    dir_files = os.listdir(directory)
    for filename in dir_files:
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            for ifile in ilist_files(file_path):
                yield ifile
        elif file_path.endswith(suffix):
            yield file_path


def get_concrete_subclasses(parent_object):
    """
    Return a list of the all the concrete (non-abstract) subclasses of
    `parent_object`. It recursively works its way to the bottom
    of the class hierarchy.

    :param object parent_object: The parent object
    :return: List of objects found
    :rtype: list
    """
    if not parent_object.__subclasses__:
        return []
    sub_classes = []
    for sub_class in parent_object.__subclasses__():
        if inspect.isabstract(sub_class):
            sub_classes.extend(get_concrete_subclasses(sub_class))
        else:
            sub_classes.append(sub_class)

    return sub_classes
