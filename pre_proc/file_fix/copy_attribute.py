"""
copy_attribute.py

Workers that fix the netCDF files that are based on the CopyGlobalAttribute or
CopyVariableAttribute abstract base classes.
"""
from .abstract import CopyGlobalAttribute, CopyVariableAttribute


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
        super().__init__(filename, directory)
        self.source_attribute = 'source_id'
        self.attribute_name = 'parent_source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'


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
        super().__init__(filename, directory)
        self.source_attribute = 'missing_value'
        self.attribute_name = '_FillValue'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'f'
