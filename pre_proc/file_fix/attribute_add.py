"""
attribute_add.py

Workers that fix the netCDF files that are based on the AttributeAdd
abstract base classes.
"""
from .abstract import AttributeAdd


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
        Set the new value.
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
        Set the new value.
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
        super(CellMeasuresAreacelloAdd, self).__init__(filename, directory)
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
        super(CellMeasuresAreacelloVolcelloAdd, self).__init__(filename,
                                                               directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
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
        Set the new value.
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
        Set the new value.
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
        super(SeaSurfaceTemperatureNameAdd, self).__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_surface_temperature'


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
        super(VarUnitsToThousandths, self).__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '0.001'


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
        super(WtemStandardNameAdd, self).__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_transformed_eulerian_mean_air_velocity'
