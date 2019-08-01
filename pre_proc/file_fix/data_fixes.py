"""
data_fixes.py

Workers that edit the data in netCDF files that are based on the DataFix
abstract base class.
"""
from abc import ABCMeta
import os
import traceback

import iris

from .abstract import NcoDataFix
from pre_proc.common import run_command
from pre_proc.exceptions import (ExistingAttributeError, Ncap2Error,
                                 NcattedError, NcpdqError)


class LatDirection(NcoDataFix):
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
        self.command = 'ncpdq -a -lat'
        self._run_nco_command(NcpdqError)


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


class ToDegC(NcoDataFix, metaclass=ABCMeta):
    """
    Abstract class to convert the data and units of a file from Kelvin to
    degrees Celsius.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        self.variable_name = None

    def apply_fix(self):
        """
        Fix the affected file

        This should replicate the Unix commands:

        ncap2 -h -s 'tos=tos-273.15f' filename.nc filename.nc.temp
        rm filename.nc
        mv filename.nc.temp filename.nc
        ncatted -h -a units,tos,m,c,'degC' filename.nc
        """
        if not self._is_kelvin():
            raise ExistingAttributeError(self.filename, 'units',
                                         'Units are not K.')

        self.command = (f"ncap2 -h -s '{self.variable_name}="
                        f"{self.variable_name}-273.15f'")
        self._run_nco_command(Ncap2Error)
        units_command = (f"ncatted -h -a units,{self.variable_name},m,c,'degC' "
                         f"{os.path.join(self.directory, self.filename)}")
        try:
            run_command(units_command)
        except Exception:
            raise NcattedError(type(self).__name__, self.filename,
                               units_command, traceback.format_exc())

    def _is_kelvin(self):
        """
        Check that the units are K currently.

        :returns: True if the units are Kelvin.
        """
        cube = iris.load_cube(os.path.join(self.directory, self.filename))
        return True if cube.units.symbol == 'K' else False


class TosToDegC(ToDegC):
    """
    Abstract class to convert the data and units of a file from Kelvin to
    degrees Celsius.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        self.variable_name = 'tos'



