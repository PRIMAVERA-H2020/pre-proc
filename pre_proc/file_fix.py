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


class AttributeUpdate(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """

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


class FurtherInfoUrlAWISourceIdAndHttps(AttributeUpdate):
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
        super(FurtherInfoUrlAWISourceIdAndHttps, self).__init__(filename,
                                                                directory)
        self.attribute_name = 'further_info_url'
        self.source_id = None
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
        self.new_value = self.new_value.replace('AWI-CM-1-0', self.source_id)

    def _get_existing_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.existing_value = getattr(rootgrp, self.attribute_name, None)
            self.source_id = getattr(rootgrp, 'source_id', None)

        if self.existing_value is None:
            raise AttributeNotFoundError(self.filename, self.attribute_name)

        if self.source_id is None:
            raise AttributeNotFoundError(self.filename, 'source_id')


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
        super(CopyAttribute, self).__init__(filename, directory)

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
        super(CopyGlobalAttribute, self).__init__(filename, directory)

    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.new_value = getattr(rootgrp, self.source_attribute, None)

        if self.new_value is None:
            raise AttributeNotFoundError(self.filename, self.source_attribute)


class ParentSourceIdFromSourceId(CopyGlobalAttribute):
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
        super(CopyVariableAttribute, self).__init__(filename, directory)

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


class FillValueFromMissingValue(CopyVariableAttribute):
    """
    Replace the _FillValue attribute value with the missing_value value.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(FillValueFromMissingValue, self).__init__(filename, directory)
        self.source_attribute = 'missing_value'
        self.attribute_name = '_FillValue'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'f'


class AttributeAdd(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    add a new metadata attribute.
    """

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


class BranchMethodAdd(AttributeAdd):
    """
    Add a global attribute `branch_method` with a value of 'no_parent'.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(BranchMethodAdd, self).__init__(filename, directory)
        self.attribute_name = 'branch_method'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'no parent'


class DataSpecsVersionAdd(AttributeAdd):
    """
    Add a global attribute `data_specs_version` with a value of '01.00.23'.

    This will probably already exist but the parent abstract class uses
    overwrite and so this should be fine.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(DataSpecsVersionAdd, self).__init__(filename, directory)
        self.attribute_name = 'data_specs_version'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = '01.00.23'


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
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'area: areacella'


class CellMeasuresAreacelloAdd(AttributeAdd):
    """
    Add a variable attribute `cellmeasures` with a value of `area: areacello`
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(CellMeasuresAreacelloAdd, self).__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'area: areacello'


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
        self.attribute_visibility = self.variable_name
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
        self.attribute_visibility = self.variable_name
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
        self.attribute_visibility = self.variable_name
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
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'sea_water_salinity'


class SeaSurfaceTemperatureNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_surface_temperature`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super(SeaSurfaceTemperatureNameAdd, self).__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 'sea_surface_temperature'


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
        self.attribute_visibility = self.variable_name
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
