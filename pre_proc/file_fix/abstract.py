"""
abstract.py

The abstract base file fixes.
"""
from abc import ABCMeta, abstractmethod
import os
import traceback

from netCDF4 import Dataset

from pre_proc.common import run_command
from pre_proc.exceptions import (AttributeNotFoundError, NcattedError,
                                 InstanceVariableNotDefinedError)


class FileFix(object, metaclass=ABCMeta):
    """
    The abstract base class that all fixes are made from
    """

    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        self.filename = filename
        self.directory = directory
        self.variable_name = self.filename.split('_')[0]

    @abstractmethod
    def apply_fix(self):
        pass


class AttributeEdit(FileFix, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        # The name of the attribute to fix
        self.attribute_name = None
        # The var_nm to pass to ncatted, e.g. global for a global
        # attribute
        self.attribute_visibility = None
        # The var_nm to pass to ncatted, e.g. global for a global
        # attribute
        self.attribute_type = None

        # The new value of the required attributes
        self.new_value = None

    @abstractmethod
    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        pass

    @abstractmethod
    def _calculate_new_value(self):
        """
        From the existing value of the attribute, calculate the new value
        """
        pass

    def _run_ncatted(self):
        """
        Run the command
        """
        for attr_name in ['attribute_name', 'attribute_visibility',
                          'new_value']:
            attr_value = getattr(self, attr_name, None)
            if attr_value is None:
                raise InstanceVariableNotDefinedError(type(self).__name__,
                                                      attr_name)

        # Aiming for:
        # ncatted -h -a branch_time_in_parent,global,o,d,10800.0

        quote_mark = "'" if isinstance(self.new_value, str) else ""

        cmd = 'ncatted -h -a {},{},{},{},{}{}{} {}'.format(
            self.attribute_name,
            self.attribute_visibility,
            'o',
            self.attribute_type,
            quote_mark,
            self.new_value,
            quote_mark,
            os.path.join(self.directory, self.filename)
        )
        try:
            run_command(cmd)
        except Exception:
            raise NcattedError(type(self).__name__, self.filename, cmd,
                               traceback.format_exc())


class AttributeUpdate(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

        # The current value of the required attributes
        self.existing_value = None

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._get_existing_value()
        self._calculate_new_value()
        self._run_ncatted()

    def _get_existing_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.existing_value = getattr(rootgrp, self.attribute_name, None)

        if self.existing_value is None:
            raise AttributeNotFoundError(self.filename, self.attribute_name)


class CopyAttribute(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """

    @abstractmethod
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

        # The name of the attribute to copy
        self.source_attribute = None

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted()

    @abstractmethod
    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        raise NotImplementedError()


class CopyGlobalAttribute(CopyAttribute, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """

    @abstractmethod
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.new_value = getattr(rootgrp, self.source_attribute, None)

        if self.new_value is None:
            raise AttributeNotFoundError(self.filename, self.source_attribute)


class CopyVariableAttribute(CopyAttribute, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """

    @abstractmethod
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        def raise_error():
            """ Raise AttributeNotFoundError """
            raise AttributeNotFoundError(
                self.filename,
                '{}.{}'.format(self.variable_name, self.source_attribute)
            )
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            netcdf_vars = getattr(rootgrp, 'variables', None)
            if netcdf_vars is None:
                raise_error()
            if self.variable_name not in netcdf_vars:
                raise_error()
            self.new_value = getattr(netcdf_vars[self.variable_name],
                                     self.source_attribute, None)
        if self.new_value is None:
            raise_error()


class AttributeAdd(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    add a new metadata attribute.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted()
