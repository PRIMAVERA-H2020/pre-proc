"""
file_fix.py

The workers that fix the netCDF files
"""
from abc import ABCMeta, abstractmethod


class FileFix(object):
    """
    The abstract base class that all fixes are made from
    """
    __metaclass__ = ABCMeta

    def __init__(self, filenames, input_dir, output_dir):
        """
        Initialise the class

        :param list filenames: The basenames as strings of the files to
            process.
        :param str input_dir: The directory that the files are
            currently in.
        :param str output_dir: The directory to save the output files
            to.
        """
        self.filenames = filenames
        self.input_dir = input_dir
        self.output_dir = output_dir

    @abstractmethod
    def apply_fix(self):
        pass


class AttEdFix(FileFix):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Initialise the class
        """
        super(AttEdFix, self).__init__()