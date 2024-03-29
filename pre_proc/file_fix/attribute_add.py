"""
attribute_add.py

Workers that fix the netCDF files that are based on the AttributeAdd
abstract base classes.
"""
import os
import re
import uuid

from netCDF4 import Dataset

from .abstract import AttributeAdd, AttributeDelete

from pre_proc.common import to_int
from pre_proc.exceptions import AttributeConversionError


class AirTemperatureNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `air_temperature`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'air_temperature'


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
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 0.0


class ParentBranchTime38714Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 38714
   (1955-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 38714.0


class ParentBranchTime40175Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 40175
   (1959-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 40175.0


class ParentBranchTime41636Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 41636
   (1963-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 41636.0


class ParentBranchTime43097Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 43097
   (1967-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 43097.0


class ParentBranchTime44558Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 44558
   (1971-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 44558.0


class ParentBranchTime45655Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 45655.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is 45655.
        """
        self.new_value = 45655.0


class ParentBranchTime46019Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 46019
   (1975-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 46019.0


class ParentBranchTime47480Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 47480
   (1979-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 47480.0


class ParentBranchTime48941Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 48941
   (1983-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 48941.0


class ParentBranchTime50402Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 50402
   (1987-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 50402.0


class ParentBranchTime51863Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of 51863
   (1991-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 51863.0


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
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 0.0


class ChildBranchTime36524Add(AttributeAdd):
    """
    Add a global attribute `branch_time_in_child` with a value of 36524 (100
    years when units are days and calendar is gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 36524.0


class ChildBranchTime38714Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 38714
   (1955-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 38714.0


class ChildBranchTime40175Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 40175
   (1959-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 40175.0


class ChildBranchTime41636Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 41636
   (1963-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 41636.0


class ChildBranchTime43097Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 43097
   (1967-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 43097.0


class ChildBranchTime44558Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 44558
   (1971-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 44558.0


class ChildBranchTime46019Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 46019
   (1975-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 46019.0


class ChildBranchTime47480Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 47480
   (1979-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 47480.0


class ChildBranchTime48941Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 48941
   (1983-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 48941.0


class ChildBranchTime50402Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 50402
   (1987-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 50402.0


class ChildBranchTime51863Add(AttributeAdd):
    """
   Add a global attribute `branch_time_in_child` with a value of 51863
   (1991-12-31 in days since 1850-1-1 and gregorian).
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        Set the new value
        """
        self.new_value = 51863.0


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
        super().__init__(filename, directory)
        self.attribute_name = 'branch_method'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'no parent'


class BranchMethodStandardAdd(AttributeAdd):
    """
    Add a global attribute `branch_method` with a value of 'standard'.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_method'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'standard'


class BranchTimeDelete(AttributeDelete):
    """
    Delete variable attribute `branch_time`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        We're deleting so there's nothing to do but make a dummy value for
        new_value.
        """
        self.new_value = 0


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
        super().__init__(filename, directory)
        self.attribute_name = 'data_specs_version'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '01.00.23'


class DataSpecsVersion27Add(AttributeAdd):
    """
    Add a global attribute `data_specs_version` with a value of '01.00.27'.

    This will probably already exist but the parent abstract class uses
    overwrite and so this should be fine.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'data_specs_version'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '01.00.27'


class DataSpecsVersion29Add(AttributeAdd):
    """
    Add a global attribute `data_specs_version` with a value of '01.00.29'.

    This will probably already exist but the parent abstract class uses
    overwrite and so this should be fine.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'data_specs_version'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '01.00.29'


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
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
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
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
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
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: areacello volume: volcello'


class CellMeasuresDelete(AttributeDelete):
    """
    Delete variable attribute `cellmeasures`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        We're deleting so there's nothing to do but make a dummy value for
        new_value.
        """
        self.new_value = 0


class CellMethodsTimeMaxAdd(AttributeAdd):
    """
    Add a variable attribute `cell_methods` with a value of `time: maximum`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing cell_methods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'time: maximum'


class CellMethodsTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of `time: mean`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'time: mean'


class CellMethodsTimePointAdd(AttributeAdd):
    """
    Add a variable attribute `cell_methods` with a value of `time: point`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing cell_methods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'time: point'


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
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: time: mean'


class CellMethodsAreaMeanTimeLandMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cell_methods` with a value of
    `area: mean where land time: mean`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    cell_methods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean where land time: mean'


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
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean where sea time: mean'


class CellMethodsAreaMeanTimePointAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: point`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean time: point'


class CellMethodsAreaTimeMeanAddLand(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: time: mean (comment: over land and sea ice)`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'area: time: mean (comment: over land and sea ice)'
        )


class CellMethodsAreaMeanTimePointAddLand(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean (comment: over land and sea ice) time: point`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'area: mean (comment: over land and sea ice) time: point'
        )


class CellMethodsAreaMeanLandTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `time: mean area: mean where land`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'time: mean area: mean where land'
        )


class CellMethodsAreaMeanLandTimePointAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean where land time: point`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'area: mean where land time: point'
        )


class CellMethodsAreaMeanTimeMinimumAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: minimum within days time: mean over days`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('area: mean time: minimum within days time: '
                          'mean over days')


class CellMethodsAreaMeanTimeMaximumAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: maximum within days time: mean over days`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('area: mean time: maximum within days time: '
                          'mean over days')


class CellMethodsAreaMeanTimeMinDailyAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: minimum`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean time: minimum'


class CellMethodsAreaMeanTimeMaxDailyAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: maximum`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean time: maximum'


class CellMethodsAreaSumSeaTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cell_methods` with a value of
    `area: sum where sea time: mean`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cell_methods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: sum where sea time: mean'


class CellMethodsIceAreaTimeMeanMaskAdd(AttributeAdd):
    """
    Add a variable attribute `cell_methods` with a value of
    `area: time: mean where sea_ice (comment: mask=siconc)`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cell_methods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: time: mean where sea_ice (comment: mask=siconc)'


class Conventions(AttributeAdd):
    """
    Add a global attribute `Conventions` with a value of
    `CF-1.7 CMIP-6.2`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'Conventions'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'CF-1.7 CMIP-6.2'


class CreationDate201807(AttributeAdd):
    """
    Add a global attribute `creation_date` with a value of
    `2018-07-01T00:00:00Z`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'creation_date'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '2018-07-01T00:00:00Z'


class DcppcAmvNegExpt(AttributeAdd):
    """
    Add a global attribute `experiment` with a value of
    `Idealized climate impact of negative 2xAMV anomaly pattern`. This is
    done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'experiment'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('Idealized climate impact of negative 2xAMV '
                          'anomaly pattern')


class DcppcAmvNegExptId(AttributeAdd):
    """
    Add a global attribute `experiment_id` with a value of
    `dcppc-amv-neg`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'experiment_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'dcppc-amv-neg'


class DcppcAmvPosExpt(AttributeAdd):
    """
    Add a global attribute `experiment` with a value of
    `Idealized climate impact of positive 2xAMV anomaly pattern`. This is
    done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'experiment'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('Idealized climate impact of positive 2xAMV '
                          'anomaly pattern')


class DcppcAmvPosExptId(AttributeAdd):
    """
    Add a global attribute `experiment_id` with a value of
    `dcppc-amv-pos`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'experiment_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'dcppc-amv-pos'


class EcEarthInstitution(AttributeAdd):
    """
    Add a global attribute `institution` with a value for EC-Earth. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'institution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, '
                          'Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany;'
                          ' ICHEC, Ireland; ICTP, Italy; IDL, Portugal; IMAU, '
                          'The Netherlands; IPMA, Portugal; KIT, Karlsruhe, '
                          'Germany; KNMI, The Netherlands; Lund University, '
                          'Sweden; Met Eireann, Ireland; NLeSC, The '
                          'Netherlands; NTNU, Norway; Oxford University, '
                          'UK; surfSARA, The Netherlands; SMHI, Sweden; '
                          'Stockholm University, Sweden; Unite ASTR, Belgium; '
                          'University College Dublin, Ireland; University of '
                          'Bergen, Norway; University of Copenhagen, Denmark; '
                          'University of Helsinki, Finland; University of '
                          'Santiago de Compostela, Spain; Uppsala University, '
                          'Sweden; Utrecht University, The Netherlands; Vrije '
                          'Universiteit Amsterdam, the Netherlands; Wageningen '
                          'University, The Netherlands. Mailing address: '
                          'EC-Earth consortium, Rossby Center, Swedish '
                          'Meteorological and Hydrological Institute/SMHI, '
                          'SE-601 76 Norrkoping, Sweden')


class EcmwfInstitution(AttributeAdd):
    """
    Add a global attribute `institution` with a value for ECMWF. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'institution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('European Centre for Medium-Range Weather '
                          'Forecasts, Reading RG2 9AX, UK')


class EcmwfReferences(AttributeAdd):
    """
    Add a global attribute `referencs` with a value for ECMWF. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'references'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('Roberts, C. D., Senan, R., Molteni, F., Boussetta, '
                          'S., Mayer, M., and Keeley, S. P. E.: Climate model '
                          'configurations of the ECMWF Integrated Forecasting '
                          'System (ECMWF-IFS cycle 43r1) for HighResMIP, '
                          'Geosci. Model Dev., 11, 3681-3712, '
                          'https://doi.org/10.5194/gmd-11-3681-2018, 2018.')


class EcmwfSourceHr(AttributeAdd):
    """
    Add a global attribute `source` with a value for ECMWF-IFS-HR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'ECMWF-IFS-HR (2017): \naerosol: none\natmos: IFS (IFS CY43R1, '
            'Tco399, cubic octahedral reduced Gaussian grid equivalent to '
            '1600 x 800 longitude/latitude; 91 levels; top level 0.01 hPa)'
            '\natmosChem: none\nland: HTESSEL (as implemented in IFS CY43R1)'
            '\nlandIce: none\nocean: NEMO3.4 (NEMO v3.4; ORCA025 tripolar grid;'
            ' 1442 x 1021 longitude/latitude; 75 levels; top grid cell 0-1 m)'
            '\nocnBgchem: none\nseaIce: LIM2 (LIM v2; ORCA025 tripolar grid; '
            '1442 x 1021 longitude/latitude)'
        )


class EcmwfSourceMr(AttributeAdd):
    """
    Add a global attribute `source` with a value for ECMWF-IFS-MR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'ECMWF-IFS-MR (2017): \naerosol: none\natmos: IFS (IFS CY43R1, '
            'Tco199, cubic octahedral reduced Gaussian grid equivalent to 800 '
            'x 400 longitude/latitude; 91 levels; top level 0.01 hPa)'
            '\natmosChem: none\nland: HTESSEL (as implemented in IFS CY43R1)'
            '\nlandIce: none\nocean: NEMO3.4 (NEMO v3.4; ORCA025 tripolar '
            'grid; 1442 x 1021 longitude/latitude; 75 levels; top grid cell '
            '0-1 m)\nocnBgchem: none\nseaIce: LIM2 (LIM v2; ORCA025 tripolar '
            'grid; 1442 x 1021 longitude/latitude)'
        )


class EcmwfSourceLr(AttributeAdd):
    """
    Add a global attribute `source` with a value for ECMWF-IFS-LR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'ECMWF-IFS-LR (2017): \naerosol: none\natmos: IFS (IFS CY43R1, '
            'Tco199, cubic octahedral reduced Gaussian grid equivalent to 800 '
            'x 400 longitude/latitude; 91 levels; top level 0.01 hPa)'
            '\natmosChem: none\nland: HTESSEL (as implemented in IFS CY43R1)'
            '\nlandIce: none\nocean: NEMO3.4 (NEMO v3.4; ORCA1 tripolar grid; '
            '362 x 292 longitude/latitude; 75 levels; top grid cell 0-1 m)'
            '\nocnBgchem: none\nseaIce: LIM2 (LIM v2; ORCA1 tripolar grid; '
            '362 x 292 longitude/latitude)'
        )


class EvapotranspirationNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `water_evapotranspiration_flux`. This is done in overwrite mode and so
    will work irrespective of whether there is an existing standard_name
    attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'water_evapotranspiration_flux'


class ExternalVariablesAreacella(AttributeAdd):
    """
    Add a global attribute `external_variables` with a value of `areacella`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'external_variables'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'areacella'


class ExternalVariablesAreacello(AttributeAdd):
    """
    Add a global attribute `external_variables` with a value of `areacello`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'external_variables'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'areacello'


class ExternalVariablesAreacelloVolcello(AttributeAdd):
    """
    Add a global attribute `external_variables` with a value of
    `areacello volcello`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'external_variables'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'areacello volcello'


class FillValueNeg999(AttributeAdd):
    """
    Add a variable attribute `_FillValue` with a value of -999. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = '_FillValue'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = -999


class ForcingIndexFromFilename(AttributeAdd):
    """
    Add a global attribute `forcing_index` with a value of
    calculated from the filename. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'forcing_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        ripf_cmpts = re.search(r'r(\d+)i(\d+)p(\d+)f(\d+)', self.filename)
        try:
            self.new_value = to_int(ripf_cmpts.group(4))
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class FrequencyDayAdd(AttributeAdd):
    """
    Add a global attribute `frequency` with a value of
    `day`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'frequency'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'day'


class FrequencyMonAdd(AttributeAdd):
    """
    Add a global attribute `frequency` with a value of
    `mon`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'frequency'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'mon'


class GeopotentialHeightNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `geopotential_height`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'geopotential_height'


class GridLabelGnAdd(AttributeAdd):
    """
    Add a global attribute `grid_label` with a value of
    `gn`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'grid_label'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'gn'


class GridLabelGrAdd(AttributeAdd):
    """
    Add a global attribute `grid_label` with a value of
    `gr`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'grid_label'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'gr'


class GridNativeAdd(AttributeAdd):
    """
    Add a global attribute `grid` with a value of
    `native atmosphere and ocean grids`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'grid'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'native atmosphere and ocean grids'


class HadGemMMParentSourceId(AttributeAdd):
    """
    Add a global attribute `parent_source_id` with a value for HadGEM3-GC31-MM.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'HadGEM3-GC31-MM'


class HistoryClearOld(AttributeAdd):
    """
    Set the global history attribute to be an empty string.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'history'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ''


class InitializationIndexFromFilename(AttributeAdd):
    """
    Add a global attribute `initialization_index` with a value of
    calculated from the filename. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'initialization_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        ripf_cmpts = re.search(r'r(\d+)i(\d+)p(\d+)f(\d+)', self.filename)
        try:
            self.new_value = to_int(ripf_cmpts.group(2))
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class MissingValueNeg999(AttributeAdd):
    """
    Add a variable attribute `missing_value` with a value of -999. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'missing_value'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = -999


class ParentActIdAdd(AttributeAdd):
    """
    Add a global attribute `parent_activity_id` with a value of
    'HighResMIP'. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_activity_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'HighResMIP'


class ParentExptIdCtrlAdd(AttributeAdd):
    """
    Add a global attribute `parent_experiment_id` with a value of
    'control-1950'. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_experiment_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'control-1950'


class ParentMipEraAdd(AttributeAdd):
    """
    Add a global attribute `parent_mip_era` with a value of
    'CMIP6'. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_mip_era'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'CMIP6'


class ParentTimeUnits1850Add(AttributeAdd):
    """
    Add a global attribute `parent_time_units` with a value of
    'days since 1850-1-1 00:00:00'. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_time_units'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'days since 1850-1-1 00:00:00'


class ParentVariantLabel(AttributeAdd):
    """
    Add a global attribute `parent_variant_label` with a value of
    'r1i1p1f1'. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_variant_label'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'r1i1p1f1'


class PhysicsIndexFromFilename(AttributeAdd):
    """
    Add a global attribute `physics_index` with a value calculated from
    the filename. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'physics_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        ripf_cmpts = re.search(r'r(\d+)i(\d+)p(\d+)f(\d+)', self.filename)
        try:
            self.new_value = to_int(ripf_cmpts.group(3))
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class PressureNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `air_pressure_at_mean_sea_level`. This is done in overwrite mode and so
    will work irrespective of whether there is an existing standard_name
    attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'air_pressure_at_mean_sea_level'


class RealizationIndexFromFilename(AttributeAdd):
    """
    Add a global attribute `realization_index` with a value of
    calculated from the filename. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'realization_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        ripf_cmpts = re.search(r'r(\d+)i(\d+)p(\d+)f(\d+)', self.filename)
        try:
            self.new_value = to_int(ripf_cmpts.group(1))
        except ValueError:
            raise AttributeConversionError(self.filename, self.attribute_name,
                                           'int')


class ProductAdd(AttributeAdd):
    """
    Add a global attribute `product` with a value of `model-output`. This is
    done in overwrite mode and so will work irrespective of whether there is
    an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'product'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'model-output'


class AtmosphereCloudIceContentStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `atmosphere_cloud_ice_content`. This is done in overwrite mode and so will
    work irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'atmosphere_cloud_ice_content'


class HfbasinpmadvStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `northward_ocean_heat_transport_due_to_parameterized_mesoscale_eddy_advection`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('northward_ocean_heat_transport_due_to_'
                          'parameterized_mesoscale_eddy_advection')


class HfbasinpmdiffStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `northward_ocean_heat_transport_due_to_parameterized_mesoscale_eddy_diffusion`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('northward_ocean_heat_transport_due_to_'
                          'parameterized_mesoscale_eddy_diffusion')


class LicenseAdd(AttributeAdd):
    """
    Add a license global attribute appropriate to the institution_id.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'license'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `PRIMAVERA`.
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            institution_id = getattr(rootgrp, 'institution_id', None)

        self.new_value = (
            f'CMIP6 model data produced by {institution_id} is licensed under '
            f'a Creative Commons Attribution-ShareAlike 4.0 International '
            f'License (https://creativecommons.org/licenses/). Consult '
            f'https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use '
            f'governing CMIP6 output, including citation requirements and '
            f'proper acknowledgment. Further information about this data, '
            f'including some limitations, can be found via the '
            f'further_info_url (recorded as a global attribute in this file). '
            f'The data producers and data providers make no warranty, either '
            f'express or implied, including, but not limited to, warranties '
            f'of merchantability and fitness for a particular purpose. All '
            f'liabilities arising from the supply of the information '
            f'(including any liability arising in negligence) are excluded to '
            f'the fullest extent permitted by law.'
        )


class MipEraToPrim(AttributeAdd):
    """
    Change the mip_era to `PRIMAVERA`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'mip_era'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `PRIMAVERA`.
        """
        self.new_value = 'PRIMAVERA'


class MpiInstitution(AttributeAdd):
    """
    Add a global attribute `institution` with a value for MPI. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'institution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('Max Planck Institute for Meteorology, '
                          'Hamburg 20146, Germany')


class MPIParentSourceIdHr(AttributeAdd):
    """
    Add a global attribute `parent_source_id` of MPI-ESM1-2-HR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'MPI-ESM1-2-HR'


class MPIParentSourceIdXr(AttributeAdd):
    """
    Add a global attribute `parent_source_id` of MPI-ESM1-2-XR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'MPI-ESM1-2-XR'


class MPISourceHr(AttributeAdd):
    """
    Add a global attribute `source` with a value for MPI-ESM1-2-HR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'MPI-ESM1.2-HR (2017): \naerosol: none, prescribed MACv2-SP\n'
            'atmos: ECHAM6.3 (spectral T127; 384 x 192 longitude/latitude; '
            '95 levels; top level 0.01 hPa)\natmosChem: none\n'
            'land: JSBACH3.20\nlandIce: none/prescribed\n'
            'ocean: MPIOM1.63 (tripolar TP04, approximately 0.4deg; '
            '802 x 404 longitude/latitude; 40 levels; top grid cell 0-12 m)\n'
            'ocnBgchem: HAMOCC\nseaIce: unnamed (thermodynamic (Semtner '
            'zero-layer) dynamic (Hibler 79) sea ice model)'
        )


class MPISourceIdHr(AttributeAdd):
    """
    Add a global attribute `source_id` of MPI-ESM1-2-HR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'MPI-ESM1-2-HR'


class MPISourceXr(AttributeAdd):
    """
    Add a global attribute `source` with a value for MPI-ESM1-2-XR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'MPI-ESM1.2-XR (2017): \naerosol: none, prescribed MACv2-SP\n'
            'atmos: ECHAM6.3 (spectral T255; 768 x 384 longitude/latitude; '
            '95 levels; top level 0.01 hPa)\natmosChem: none\n'
            'land: JSBACH3.20\nlandIce: none/prescribed\n'
            'ocean: MPIOM1.63 (tripolar TP04, approximately 0.4deg; '
            '802 x 404 longitude/latitude; 40 levels; top grid cell 0-12 m)\n'
            'ocnBgchem: HAMOCC6\nseaIce: unnamed (thermodynamic (Semtner '
            'zero-layer) dynamic (Hibler 79) sea ice model)'
        )


class MPISourceIdXr(AttributeAdd):
    """
    Add a global attribute `source_id` of MPI-ESM1-2-XR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'MPI-ESM1-2-XR'


class MsftmzmpaStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `ocean_meridional_overturning_mass_streamfunction_due_to_parameterized_
    mesoscale_eddy_advection`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('ocean_meridional_overturning_mass_streamfunction_'
                          'due_to_parameterized_mesoscale_eddy_advection')


class NominalResolution100km(AttributeAdd):
    """
    Change the nominal_resolution to `100 km`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'nominal_resolution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `100 km`.
        """
        self.new_value = '100 km'


class NominalResolution50km(AttributeAdd):
    """
    Change the nominal_resolution to `50 km`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'nominal_resolution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `50 km`.
        """
        self.new_value = '50 km'


class NominalResolution25km(AttributeAdd):
    """
    Change the nominal_resolution to `25 km`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'nominal_resolution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `25 km`.
        """
        self.new_value = '25 km'


class NominalResolution10km(AttributeAdd):
    """
    Change the nominal_resolution to `10 km`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'nominal_resolution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `10 km`.
        """
        self.new_value = '10 km'


class RealmAtmos(AttributeAdd):
    """
    Change the realm to `atmos`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'realm'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `atmos`.
        """
        self.new_value = 'atmos'


class RealmOcean(AttributeAdd):
    """
    Change the realm to `ocean`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'realm'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `ocean`.
        """
        self.new_value = 'ocean'


class RealmSeaIce(AttributeAdd):
    """
    Change the realm to `seaIce`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'realm'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Change the existing value to `ocean`.
        """
        self.new_value = 'seaIce'


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
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
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
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_surface_temperature'


class ShallowConvectivePrecipitationFluxStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `shallow_convective_precipitation_flux`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'shallow_convective_precipitation_flux'


class SidmassdynStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `tendency_of_sea_ice_amount_due_to_sea_ice_dynamics`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'tendency_of_sea_ice_amount_due_to_sea_ice_dynamics'


class SidmassthStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `tendency_of_sea_ice_amount_due_to_sea_ice_thermodynamics`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('tendency_of_sea_ice_amount_due_to_sea_ice_'
                          'thermodynamics')


class SiflcondbotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_ice_basal_net_downward_sensible_heat_flux`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_ice_basal_net_downward_sensible_heat_flux'


class SiflfwbotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `water_flux_into_sea_water_from_sea_ice`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'water_flux_into_sea_water_from_sea_ice'


class SiflsensupbotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `upward_sea_ice_basal_heat_flux`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_sea_ice_basal_heat_flux'


class SihcStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_ice_temperature_expressed_as_heat_content`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_ice_temperature_expressed_as_heat_content'


class SisaltmassStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_ice_salt_content`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_ice_salt_content'


class SistrxubotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `upward_x_stress_at_sea_ice_base`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_x_stress_at_sea_ice_base'


class SistryubotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `upward_y_stress_at_sea_ice_base`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_y_stress_at_sea_ice_base'


class SitempbotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_ice_basal_temperature`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_ice_basal_temperature'


class SoilMoistureNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `mass_content_of_water_in_soil`. This is done in overwrite mode and so
    will work irrespective of whether there is an existing standard_name
    attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'mass_content_of_water_in_soil'


class SourceTypeAogcmAdd(AttributeAdd):
    """
    Add a global attribute `source_type` with a value of `AOGCM`. This is
    done in overwrite mode and so will work irrespective of whether there
    is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source_type'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'AOGCM'


class SpecificHumidityStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `specific_humidity`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'specific_humidity'


class SitimefracStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `fraction_of_time_with_sea_ice_area_fraction_above_threshold`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('fraction_of_time_with_sea_ice_area_fraction_'
                          'above_threshold')


class SubExperiment(AttributeAdd):
    """
    Add a global attribute `sub_experiment` with a value of
    `none`. This is done in overwrite mode and so will work irrespective of
    whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'sub_experiment'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'none'


class SubExperimentId(AttributeAdd):
    """
    Add a global attribute `sub_experiment_id` with a value of
    `none`. This is done in overwrite mode and so will work irrespective of
    whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'sub_experiment_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'none'


class SurfaceTemperatureNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `surface_temperature`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'surface_temperature'


class TableIdAdd(AttributeAdd):
    """
    Add a global attribute `table_id` with an appropriate value determined
    from the filename. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'table_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = self.filename.split('_')[1]


class TrackingIdNew(AttributeAdd):
    """
    Replace the tracking_id attribute with a new value. This may be useful
    when resubmitting files that have been retracted.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'tracking_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = f'hdl:21.14100/{uuid.uuid4()}'


class UaStdNameAdd(AttributeAdd):
    """
    Replace the variable's `standard_name` with `eastward_wind`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'eastward_wind'


class VariableIdAdd(AttributeAdd):
    """
    Add a global attribute `variable_id` with an appropriate value determined
    from the filename. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'variable_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = self.filename.split('_')[0]


class VariantLabelFromFilename(AttributeAdd):
    """
    Add a global attribute `forcing_index` with a value of
    calculated from the filename. This is done in overwrite mode and
    so will work irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'variant_label'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        ripf_cmpts = re.search(r'r(\d+)i(\d+)p(\d+)f(\d+)', self.filename)
        self.new_value = (f'r{ripf_cmpts.group(1)}'
                          f'i{ripf_cmpts.group(2)}'
                          f'p{ripf_cmpts.group(3)}'
                          f'f{ripf_cmpts.group(4)}')


class VarUnitsTo1(AttributeAdd):
    """
    Replace the variable's attribute `units` to `1`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '1'


class VarUnitsToDegC(AttributeAdd):
    """
    Replace the variable's attribute `units` to `degC`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'degC'


class VarUnitsToKelvin(AttributeAdd):
    """
    Replace the variable's attribute `units` with `K`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'K'


class VarUnitsToMetre(AttributeAdd):
    """
    Replace the variable's attribute `units` with `m`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'm'


class VarUnitsToMetrePerSecond(AttributeAdd):
    """
    Replace the variable's attribute `units` with `m s-1`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'm s-1'


class VarUnitsToPascalPerSecond(AttributeAdd):
    """
    Replace the variable's attribute `units` to `Pa s-1`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'Pa s-1'


class VarUnitsToPercent(AttributeAdd):
    """
    Replace the variable's attribute `units` to `%`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '%'


class VarUnitsToThousandths(AttributeAdd):
    """
    Replace the variable's attribute `units` to `0.001`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '0.001'


class VaStdNameAdd(AttributeAdd):
    """
    Replace the variable's `standard_name` with `northward_wind`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'northward_wind'


class VerticesLatStdNameDelete(AttributeDelete):
    """
    Delete `standard_name` attribute from `vertices_latitude`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = 'vertices_latitude'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        We're deleting so there's nothing to do but make a dummy value for
        new_value.
        """
        self.new_value = 0


class VerticesLonStdNameDelete(AttributeDelete):
    """
    Delete `standard_name` attribute from `vertices_longitude`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = 'vertices_longitude'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        We're deleting so there's nothing to do but make a dummy value for
        new_value.
        """
        self.new_value = 0


class WapStandardNameAdd(AttributeAdd):
    """
    Replace the variable's `standard_name` with
    `lagrangian_tendency_of_air_pressure`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'lagrangian_tendency_of_air_pressure'


class WtemStandardNameAdd(AttributeAdd):
    """
    Replace the variable's `standard_name` with
    `upward_transformed_eulerian_mean_air_velocity`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_transformed_eulerian_mean_air_velocity'


class WindSpeedStandardNameAdd(AttributeAdd):
    """
    Replace the variable's `standard_name` with
    `wind_speed`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'wind_speed'


class ZFurtherInfoUrl(AttributeAdd):
    """
    Add a global attribute `further_info_url` with a value generated
    correctly from existing other attributes in the file. This is done
    in overwrite mode and so will work irrespective of whether there
    is an existing attribute. The Z at the start of the name allows it
    to run after other fixes so that the necessary attributes have
    already been fixed.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'further_info_url'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            mip_era = getattr(rootgrp, 'mip_era', None)
            institution_id = getattr(rootgrp, 'institution_id', None)
            source_id = getattr(rootgrp, 'source_id', None)
            experiment_id = getattr(rootgrp, 'experiment_id', None)
            sub_experiment_id = getattr(rootgrp, 'sub_experiment_id', None)
            variant_label = getattr(rootgrp, 'variant_label', None)

        self.new_value = (f'https://furtherinfo.es-doc.org/'
                          f'{mip_era}.'
                          f'{institution_id}.'
                          f'{source_id}.'
                          f'{experiment_id}.'
                          f'{sub_experiment_id}.'
                          f'{variant_label}')


class ZZZThetapv2StandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `theta_on_pv2_surface`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute. This has to be done after ZZZEcEarthLongitudeFix,
    which removes this standard_name

    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'theta_on_pv2_surface'
