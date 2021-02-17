"""
data_fixes.py

Workers that edit the data in netCDF files that are based on the DataFix
abstract base class.
"""
import os
import traceback
import warnings

import iris

from .abstract import (DataFix, FixHadGEMMask, NcoDataFix, NcksAppendDataFix,
                       RemoveHalo, InsertHadGEMGrid)
from pre_proc.common import run_command
from pre_proc.exceptions import (ExistingAttributeError, CdoError, Ncap2Error,
                                 NcattedError, NcpdqError, NcksError,
                                 NcrenameError)

from highresmip_fix.fix_latlon_atmosphere import (fix_latlon_atmosphere,
                                                  binary_size)
import fix_lons

# Ignore warnings displayed when loading data into Iris to check it
warnings.filterwarnings("ignore")

# The directory where the byte masks are stored
BYTE_MASK_DIR = '/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/bytes_masks'
# The directories where the known good grids to paste in are stored
NEMO_GRID_DIR = '/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/grids'
CICE_COORDS_DIR = ('/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/'
                   'cice_coords')
CICE_MASK_DIR = '/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/cice_masks'

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


class AAVarNameToFileName(NcoDataFix):
    """
    Rename the variable itself and variable_id global attribute to the first
    component of the filename.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Rename the variable and then the global attribute
        """
        var_name = self.filename.split('_')[0]
        existing_name = self._get_existing_name()

        self.command = f'ncrename -h -v {existing_name},{var_name}'
        self._run_nco_command(NcrenameError)

        self.command = f'ncatted -h -a variable_id,global,m,c,{var_name}'
        self._run_nco_command(NcattedError)

    def _get_existing_name(self):
        """
        Get the global attribute variable_id
        """
        cube = iris.load_cube(os.path.join(self.directory, self.filename))
        return cube.attributes['variable_id']


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


class ZZZAddHeight2m(NcksAppendDataFix):
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


class AAARemoveOrca1Halo(RemoveHalo):
    """
    Remove the halo from files on the HadGEM ORCA1 grid. AAA in the class'
    name causes it to run first.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_row_spec(self):
        """Set the row specification"""
        self.row_spec = '-di,1,360 -dj,1,330'


class AAARemoveOrca025Halo(RemoveHalo):
    """
    Remove the halo from files on the HadGEM ORCA025 grid. AAA in the class'
    name causes it to run first.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_row_spec(self):
        """Set the row specification"""
        self.row_spec = '-di,1,1440 -dj,1,1205'


class FixMaskOrca1TSurface(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA1 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_2D_T'


class FixMaskOrca025TSurface(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA025 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_2D_T'


class FixMaskOrca1USurface(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA1 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_2D_U'


class FixMaskOrca1USingleLevel(FixHadGEMMask):
    """
    Fix the mask for single level data on the ORCA1 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_single_level_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_U'


class FixMaskOrca025USurface(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA025 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_2D_U'


class FixMaskOrca025USingleLevel(FixHadGEMMask):
    """
    Fix the mask for single level data on the ORCA025 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_single_level_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_U'


class FixMaskOrca1VSurface(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA1 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_2D_V'


class FixMaskOrca1VSingleLevel(FixHadGEMMask):
    """
    Fix the mask for single level data on the ORCA1 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_single_level_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_V'


class FixMaskOrca025VSurface(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA025 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_2D_V'


class FixMaskOrca025VSingleLevel(FixHadGEMMask):
    """
    Fix the mask for single level data on the ORCA025 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_single_level_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_V'


class FixMaskOrca1TOlevel(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA1 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_T'


class FixMaskOrca025TOlevel(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA025 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_T'


class FixMaskOrca1UOlevel(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA1 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_U'


class FixMaskOrca025UOlevel(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA025 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_U'


class FixMaskOrca1VOlevel(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA1 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-LL/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_V'


class FixMaskOrca025VOlevel(FixHadGEMMask):
    """
    Fix the mask for data on the ORCA025 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            BYTE_MASK_DIR,
            'HadGEM3-GC31-MM/primavera_byte_masks.nc'
        )
        self.mask_var_name = 'mask_3D_V'


class FixGridOrca1T(InsertHadGEMGrid):
    """
    Fix the grid for data on the HadGEM ORCA1 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(NEMO_GRID_DIR,
                                            'ORCA1/ORCA1_grid-t.nc')


class FixGridOrca025T(InsertHadGEMGrid):
    """
    Fix the grid for data on the HadGEM ORCA025 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(NEMO_GRID_DIR,
                                            'ORCA025/ORCA025_grid-t.nc')


class FixGridOrca1U(InsertHadGEMGrid):
    """
    Fix the grid for data on the HadGEM ORCA1 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(NEMO_GRID_DIR,
                                            'ORCA1/ORCA1_grid-u.nc')


class FixGridOrca025U(InsertHadGEMGrid):
    """
    Fix the grid for data on the HadGEM ORCA025 u-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(NEMO_GRID_DIR,
                                            'ORCA025/ORCA025_grid-u.nc')


class FixGridOrca1V(InsertHadGEMGrid):
    """
    Fix the grid for data on the HadGEM ORCA1 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(NEMO_GRID_DIR,
                                            'ORCA1/ORCA1_grid-v.nc')


class FixGridOrca025V(InsertHadGEMGrid):
    """
    Fix the grid for data on the HadGEM ORCA025 v-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(NEMO_GRID_DIR,
                                            'ORCA025/ORCA025_grid-v.nc')


class FixCiceCoords1T(InsertHadGEMGrid):
    """
    Fix the coords for CICE data on the HadGEM ORCA1 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(
            CICE_COORDS_DIR,
            'eORCA1/cice_eORCA1_coords_grid-t.nc'
        )


class FixCiceCoords1UV(InsertHadGEMGrid):
    """
    Fix the coords for CICE data on the HadGEM ORCA1 u and v-grids.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(
            CICE_COORDS_DIR,
            'eORCA1/cice_eORCA1_coords_grid-uv.nc'
        )


class FixCiceCoords025T(InsertHadGEMGrid):
    """
    Fix the coords for CICE data on the HadGEM ORCA025 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(
            CICE_COORDS_DIR,
            'eORCA025/cice_eORCA025_coords_grid-t.nc'
        )


class FixCiceCoords025UV(InsertHadGEMGrid):
    """
    Fix the coords for CICE data on the HadGEM ORCA025 u and v-grids.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(
            CICE_COORDS_DIR,
            'eORCA025/cice_eORCA025_coords_grid-uv.nc'
        )


class FixCiceCoords12T(InsertHadGEMGrid):
    """
    Fix the coords for CICE data on the HadGEM ORCA12 t-grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(
            CICE_COORDS_DIR,
            'eORCA12/cice_eORCA12_coords_grid-t.nc'
        )


class FixCiceCoords12UV(InsertHadGEMGrid):
    """
    Fix the coords for CICE data on the HadGEM ORCA12 u and v-grids.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_known_good(self):
        """Set the known good grid"""
        self.known_good_file = os.path.join(
            CICE_COORDS_DIR,
            'eORCA12/cice_eORCA12_coords_grid-uv.nc'
        )


class FixMaskCICEOrca1UV(FixHadGEMMask):
    """
    Fix the mask for data on the CICE ORCA1 u and v grids.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            CICE_MASK_DIR,
            'primavera_cice_orca1_uv.nc'
        )
        self.mask_var_name = 'mask'


class FixMaskCICEOrca025T(FixHadGEMMask):
    """
    Fix the mask for data on the CICE ORCA025 t grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            CICE_MASK_DIR,
            'primavera_cice_orca025_t.nc'
        )
        self.mask_var_name = 'mask'


class FixMaskCICEOrca12T(FixHadGEMMask):
    """
    Fix the mask for data on the CICE ORCA12 t grid.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)

    def _set_byte_mask(self):
        """Set the mask file and name"""
        self.byte_mask_file = os.path.join(
            CICE_MASK_DIR,
            'primavera_cice_orca12_t.nc'
        )
        self.mask_var_name = 'mask'
