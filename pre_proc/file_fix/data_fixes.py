"""
data_fixes.py

Workers that edit the data in netCDF files that are based on the DataFix
abstract base class.
"""
import os
import traceback
import warnings

import iris

from .abstract import NcoDataFix
from pre_proc.common import run_command
from pre_proc.exceptions import (ExistingAttributeError, Ncap2Error,
                                 NcattedError, NcpdqError, NcksError)

# Ignore warnings displayed when loading data into Iris to check it
warnings.filterwarnings("ignore")


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
        Run ncpdq and then swap the columns in lat_bnds.
        """
        # check that the latitude is decreasing and that the fix is actually
        # needed
        if not self._is_lat_decreasing():
            raise ExistingAttributeError(self.filename, 'latitude',
                                         'Latitude is not decreasing.')
        self.command = 'ncpdq -a -lat'
        self._run_nco_command(NcpdqError)

        original_nc = os.path.join(self.directory, self.filename)
        bnds_file = original_nc + '.bnds'
        corrected_bnds_file = bnds_file + '_corr'

        # Remove any temporary files left over from a previous failed
        # run as they can prevent ncks and ncpdq from running.
        for filename in (bnds_file, corrected_bnds_file):
            if os.path.exists(filename):
                os.remove(filename)

        commands = [
            # Copy lat_bnds to a new file
            f'ncks -v lat_bnds {original_nc} {bnds_file}',
            # Swap the colums
            f'ncpdq -a -bnds {bnds_file} {corrected_bnds_file}',
            # Remove history from lat_bnds as this is pasted back into the file
            f'ncatted -h -a history,global,d,, {corrected_bnds_file}',
            # Paste the fixed bnds back into the original file
            f'ncks -A -v lat_bnds {corrected_bnds_file} {original_nc}'
        ]
        for cmd in commands:
            try:
                run_command(cmd)
            except Exception:
                exceptions = {
                    'ncks': NcksError,
                    'ncpdq': NcpdqError,
                    'ncatted': NcattedError
                }
                cmd_name = cmd.split()[0]
                raise exceptions[cmd_name](type(self).__name__, self.filename,
                                           cmd, traceback.format_exc())
        os.remove(bnds_file)
        os.remove(corrected_bnds_file)

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


class ToDegC(NcoDataFix):
    """
    Convert the data and units of a file from Kelvin to degrees Celsius.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

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
