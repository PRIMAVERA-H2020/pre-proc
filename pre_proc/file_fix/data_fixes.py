"""
data_fixes.py

Workers that edit the data in netCDF files that are based on the DataFix
abstract base class.
"""
import os
import shutil
import traceback
import warnings

import iris

from .abstract import DataFix, NcoDataFix, NcksDataFix
from pre_proc.common import run_command
from pre_proc.exceptions import (ExistingAttributeError, CdoError, Ncap2Error,
                                 NcattedError, NcpdqError, NcksError,
                                 NcrenameError)

from highresmip_fix.fix_latlon_atmosphere import (fix_latlon_atmosphere,
                                                  binary_size)
import fix_lons

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


class LevToPlev(NcoDataFix):
    """
    Rename the lev dimension and variable to plev.
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
        self.command = 'ncrename -h -d lev,plev -v lev,plev'
        self._run_nco_command(NcrenameError)


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


class ZZEcEarthAtmosFix(DataFix):
    """
    Use the EC-Earth provided module to convert the EC-Earth 2D latitude and
    longitudes into scalar coordinates. The ZZ at the start of the name causes
    this to be one of the last fixes to run.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

        # Use the default chunk size
        self.default_chunk_size = '64KiB'

    def apply_fix(self):
        """
        Fix the affected file
        """
        fix_latlon_atmosphere(
            os.path.join(self.directory, self.filename),
            binary_size(self.default_chunk_size)
        )


class ZZZEcEarthLongitudeFix(DataFix):
    """
    Use the EC-Earth provided module to fix the EC-Earth longitude. The ZZZ
    at the start of the name causes this to be the last fix to run.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Fix the affected file
        """
        fix_lons.fix_file(
            os.path.join(self.directory, self.filename),
            write=True,
            keepid=True
        )


class SetTimeReference1949(NcoDataFix):
    """
    Set the reference time of the time variable to be 1949-01-01
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Use cdo to set the reference time.
        """
        self.command = "cdo -z zip_3 -setreftime,'1949-01-01','00:00:00'"
        self._run_nco_command(CdoError)


class ZZZAddHeight2m(NcksDataFix):
    """
    Add a heighr2m dimension from the reference file.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        self.reference_file = (
            '/gws/nopw/j04/primavera1/cache/jseddon/reference_files/'
            'height2m_reference.nc'
        )

    def apply_fix(self):
        """
        Use cdo to set the reference time.
        """
        self.command = f"ncks -h -A -v height {self.reference_file}"
        self._run_ncks_command()

        units_command = (f"ncatted -h -a coordinates,{self.variable_name},o,c,"
                         f"'height' "
                         f"{os.path.join(self.directory, self.filename)}")
        try:
            run_command(units_command)
        except Exception:
            raise NcattedError(type(self).__name__, self.filename,
                               units_command, traceback.format_exc())


class RemoveHalo(NcoDataFix, metaclass=ABCMeta):
    """
    Rename the lev dimension and variable to plev.
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
    self.command = "cdo -z zip_3 -setreftime,'1949-01-01','00:00:00'"
    self._run_nco_command(CdoError)
