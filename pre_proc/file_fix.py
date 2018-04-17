"""
file_fix.py

The workers that fix the netCDF files
"""
from abc import ABCMeta, abstractmethod
import os
import re

from netCDF4 import Dataset

from pre_proc.common import run_command
from pre_proc.exceptions import (AttributeNotFoundError,
                                 AttributeConversionError,
                                 ExistingAttributeError,
                                 InstanceVariableNotDefinedError)


class FileFix(object):
    """
    The abstract base class that all fixes are made from
    """
    __metaclass__ = ABCMeta

    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        self.filename = filename
        self.directory = directory

    @abstractmethod
    def apply_fix(self):
        pass


class AttributeEdit(FileFix):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """
    __metaclass__ = ABCMeta

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super(AttributeEdit, self).__init__(filename, directory)
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
        run_command(cmd)


class AttributeUpdate(AttributeEdit):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """
    __metaclass__ = ABCMeta

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super(AttributeUpdate, self).__init__(filename, directory)

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


class ParentBranchTimeDoubleFix(AttributeUpdate):
    """
    Make the global attribute `branch_time_in_parent` a double
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(ParentBranchTimeDoubleFix, self).__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = _to_float(self.existing_value)
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'float')


class ChildBranchTimeDoubleFix(AttributeUpdate):
    """
    Make the global attribute `branch_time_in_child` a double
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(ChildBranchTimeDoubleFix, self).__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = _to_float(self.existing_value)
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'float')


class ForcingIndexIntFix(AttributeUpdate):
    """
    Make the global attribute `forcing_index` an int.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(ForcingIndexIntFix, self).__init__(filename, directory)
        self.attribute_name = 'forcing_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = _to_int(self.existing_value)
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class InitializationIndexIntFix(AttributeUpdate):
    """
    Make the global attribute `initialization_index` an int.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(InitializationIndexIntFix, self).__init__(filename, directory)
        self.attribute_name = 'initialization_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = _to_int(self.existing_value)
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class PhysicsIndexIntFix(AttributeUpdate):
    """
    Make the global attribute `physics_index` an int.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(PhysicsIndexIntFix, self).__init__(filename, directory)
        self.attribute_name = 'physics_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = _to_int(self.existing_value)
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class RealizationIndexIntFix(AttributeUpdate):
    """
    Make the global attribute `realization_index` an int.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(RealizationIndexIntFix, self).__init__(filename, directory)
        self.attribute_name = 'realization_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = _to_int(self.existing_value)
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class FurtherInfoUrlToHttps(AttributeUpdate):
    """
    Change the protocol in the further_info_url attribute from HTTP to
    HTTPS.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(FurtherInfoUrlToHttps, self).__init__(filename, directory)
        self.attribute_name = 'further_info_url'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        if not self.existing_value.startswith('http:'):
            raise ExistingAttributeError(self.filename, self.attribute_name,
                                         'Existing further_info_url attribute '
                                         'does not start with http:')

        self.new_value = self.existing_value.replace('http:', 'https:', 1)


class CopyAttribute(AttributeEdit):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """
    __metaclass__ = ABCMeta

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super(CopyAttribute, self).__init__(filename, directory)

        # The name of the attribute to copy
        self.source_attribute = None

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted()

    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.new_value = getattr(rootgrp, self.source_attribute, None)

        if self.new_value is None:
            raise AttributeNotFoundError(self.filename, self.source_attribute)


class ParentSourceIdFromSourceId(CopyAttribute):
    """
    Replace the parent_source_id attribute value with the source_id value.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(ParentSourceIdFromSourceId, self).__init__(filename, directory)
        self.source_attribute = 'source_id'
        self.attribute_name = 'parent_source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'


class AttributeAdd(AttributeEdit):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    add a new metadata attribute.
    """
    __metaclass__ = ABCMeta

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super(AttributeAdd, self).__init__(filename, directory)

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted()


class ParentBranchTimeAdd(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of zero.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(ParentBranchTimeAdd, self).__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 0.0


class ChildBranchTimeAdd(AttributeAdd):
    """
    Add a global attribute `branch_time_in_child` with a value of zero.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(ChildBranchTimeAdd, self).__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 0.0


class CellMeasuresAreacellaAdd(AttributeAdd):
    """
    Add a variable attribute `cellmeasures` with a value of `area: areacella`
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(CellMeasuresAreacellaAdd, self).__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = filename.split('_')[0]
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'area: areacella'


class CellMeasuresAreacelloVolcelloAdd(AttributeAdd):
    """
    Add a variable attribute `cellmeasures` with a value of
    `area: areacello volume: volcello`
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(CellMeasuresAreacelloVolcelloAdd, self).__init__(filename,
                                                               directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = filename.split('_')[0]
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'area: areacello volume: volcello'


class CellMethodsAreaTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of `area: time: mean`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(CellMethodsAreaTimeMeanAdd, self).__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = filename.split('_')[0]
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'area: time: mean'


class CellMethodsSeaAreaTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean where sea time: mean`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(CellMethodsSeaAreaTimeMeanAdd, self).__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = filename.split('_')[0]
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'area: mean where sea time: mean'


class SeaWaterSalinityStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_water_salinity`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(SeaWaterSalinityStandardNameAdd, self).__init__(filename,
                                                              directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = filename.split('_')[0]
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'sea_water_salinity'


class VarUnitsToThousandths(AttributeAdd):
    """
    Replace the variable's attribute `units` to `0.001`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(VarUnitsToThousandths, self).__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = filename.split('_')[0]
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = '0.001'


def _to_float(string_value):
    """
    Convert a string starting with a float to a float and return this.

    :param str string_value: The string to convert.
    :returns: The float from the start of the string.
    :rtype: float
    :raises ValueError: if a float cannot be found.
    """
    float_regexp = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
    try:
        float_component = re.match(float_regexp, string_value).group(0)
    except AttributeError:
        raise ValueError('Cannot find float in {}'.format(string_value))

    return float(float_component)


def _to_int(string_value):
    """
    Convert a string starting with an int to an int and return this.

    :param str string_value: The string to convert.
    :returns: The int from the start of the string.
    :rtype: int
    :raises ValueError: if an int cannot be found.
    """
    int_regexp = r'[+-]?(\d+)'
    try:
        int_component = re.match(int_regexp, string_value).group(0)
    except AttributeError:
        raise ValueError('Cannot find int in {}'.format(string_value))

    return int(int_component)
