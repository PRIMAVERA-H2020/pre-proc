"""
attribute_update.py

Workers that fix the netCDF files that are based on the AttributeUpdate
abstract base class.
"""
import os

from netCDF4 import Dataset

from pre_proc.common import to_float, to_int
from pre_proc.exceptions import (AttributeNotFoundError,
                                 AttributeConversionError,
                                 ExistingAttributeError)
from .abstract import AttributeUpdate


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
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = to_float(self.existing_value)
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
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = to_float(self.existing_value)
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
        super().__init__(filename, directory)
        self.attribute_name = 'forcing_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = to_int(self.existing_value)
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
        super().__init__(filename, directory)
        self.attribute_name = 'initialization_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = to_int(self.existing_value)
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
        super().__init__(filename, directory)
        self.attribute_name = 'physics_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = to_int(self.existing_value)
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
        super().__init__(filename, directory)
        self.attribute_name = 'realization_index'
        self.attribute_visibility = 'global'
        self.attribute_type = 's'

    def _calculate_new_value(self):
        """
        The new value is the existing string converted to a double.
        """
        try:
            self.new_value = to_int(self.existing_value)
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
        super().__init__(filename, directory)
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
        super().__init__(filename,
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


class AogcmToAgcm(AttributeUpdate):
    """
    Change the global attribute `source_type` from `AOGCM` to `AGCM`.
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
        Check the existing attribute is `AOGCM` and change it to `AGCM`.
        """
        if self.existing_value != 'AOGCM':
            raise ExistingAttributeError(self.filename, self.attribute_name,
                                           'Existing value is not AOGCM.')
        else:
            self.new_value = 'AGCM'


class TrackingIdFix(AttributeUpdate):
    """
    Convert the tracking_id to the correct form.
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
        Convert the tracking_id to the correct form.
        """
        if self.existing_value.startswith('hdl:'):
            raise ExistingAttributeError(self.filename, self.attribute_name,
                                         'Existing tracking_id attribute '
                                         'starts with hdl:')

        self.new_value = 'hdl:21.14100/{}'.format(self.existing_value)
