"""
data_fixes.py

Workers that edit the data in netCDF files that are based on the DataFix
abstract base class.
"""
import os
import traceback

import iris

from .abstract import DataFix
from pre_proc.common import run_command
from pre_proc.exceptions import NcpdqError, ExistingAttributeError


class LatDirection(DataFix):
    """
    Reverse the direction of the latitude dimension using ncpdq.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Run ncpdq.
        """
        # check that the latitude is decreasing and that the fix is actually
        # needed
        if not self._is_lat_decreasing():
            raise ExistingAttributeError(self.filename, 'latitude',
                                         'Latitude is not decreasing.')

        output_file = os.path.join(self.directory, self.filename)
        temp_file = output_file + '.temp'
        cmd = 'ncpdq -a -lat {} {}'.format(output_file, temp_file)
        try:
            run_command(cmd)
        except Exception:
            raise NcpdqError(type(self).__name__, self.filename, cmd,
                             traceback.format_exc())

        os.remove(output_file)
        os.rename(temp_file, output_file)

    def _is_lat_decreasing(self):
        """
        Check that the latitude co-ordinate is decreasing.

        :returns: True if the latitude coordinate is decreasing.
        """
        cube = iris.load_cube(os.path.join(self.directory, self.filename))
        lat_coord = cube.coord('latitude')
        if lat_coord.points[0] > lat_coord.points[1]:
            return True
        else:
            return False
