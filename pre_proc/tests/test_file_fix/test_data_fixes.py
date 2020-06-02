"""
test_data_fixes.py

Unit tests for all FileFix concrete classes from data_fixes.py
"""
import subprocess
import unittest
from unittest import mock

import cf_units
from iris.tests.stock import realistic_3d
import numpy as np

from pre_proc.exceptions import ExistingAttributeError, NcksError
from pre_proc.file_fix import (LatDirection, LevToPlev, AAVarNameToFileName,
                               ToDegC, ZZEcEarthAtmosFix,
                               ZZZEcEarthLongitudeFix,
                               SetTimeReference1949, ZZZAddHeight2m,
                               AAARemoveOrca1Halo, AAARemoveOrca025Halo,
                               FixMaskOrca1TSurface, FixMaskOrca025TSurface,
                               FixMaskOrca1TOlevel, FixMaskOrca025TOlevel,
                               FixMaskOrca1USurface, FixMaskOrca025USurface,
                               FixMaskOrca1UOlevel, FixMaskOrca025UOlevel,
                               FixMaskOrca1VSurface, FixMaskOrca025VSurface,
                               FixMaskOrca1VOlevel, FixMaskOrca025VOlevel,
                               FixGridOrca1T, FixGridOrca025T,
                               FixGridOrca1U, FixGridOrca025U,
                               FixGridOrca1V, FixGridOrca025V,
                               FixCiceCoords1T, FixCiceCoords1UV,
                               FixMaskOrca1USingleLevel,
                               FixMaskOrca1VSingleLevel,
                               FixMaskOrca025USingleLevel,
                               FixMaskOrca025VSingleLevel)


class NcoDataFixBaseTest(unittest.TestCase):
    """
    Base class to setup a typical environment used by other tests
    """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.remove')
        self.mock_remove = patch.start()
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.rename')
        self.mock_rename = patch.start()
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.path.exists')
        self.mock_exists = patch.start()
        self.mock_exists.return_value = False
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.abstract.shutil.copyfile')
        self.mock_copyfile = patch.start()
        self.mock_copyfile.return_value = False
        self.addCleanup(patch.stop)


class TestLatDirection(NcoDataFixBaseTest):
    """
    Test LatDirection main functionality
    """
    def setUp(self):
        """ Use NcoDataFixBaseTest but also patch the unique external calls """
        super().setUp()

        patch = mock.patch('pre_proc.file_fix.data_fixes.LatDirection.'
                           '_is_lat_decreasing')
        self.mock_lat_check = patch.start()
        self.mock_lat_check.return_value = True
        self.addCleanup(patch.stop)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        LatDirection
        """
        fix = LatDirection('1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call('ncpdq -a -lat /a/1.nc /a/1.nc.temp',
                      stderr=subprocess.STDOUT, shell=True),
            mock.call('ncks -v lat_bnds /a/1.nc /a/1.nc.bnds',
                      stderr=subprocess.STDOUT, shell=True),
            mock.call('ncpdq -a -bnds /a/1.nc.bnds /a/1.nc.bnds_corr',
                      stderr=subprocess.STDOUT, shell=True),
            mock.call('ncatted -h -a history,global,d,, /a/1.nc.bnds_corr',
                      stderr=subprocess.STDOUT, shell=True),
            mock.call('ncks -A -v lat_bnds /a/1.nc.bnds_corr /a/1.nc',
                      stderr=subprocess.STDOUT, shell=True)
        ]
        self.mock_subprocess.assert_has_calls(calls)

    def test_remove_called_correctly(self):
        """
        Test that input files is removed.
        """
        fix = LatDirection('1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call('/a/1.nc'),
            mock.call('/a/1.nc.bnds'),
            mock.call('/a/1.nc.bnds_corr')
        ]
        self.mock_remove.assert_has_calls(calls)

    def test_rename_called_correctly(self):
        """
        Test that output file is renamed.
        """
        fix = LatDirection('1.nc', '/a')
        fix.apply_fix()
        self.mock_rename.assert_called_once_with('/a/1.nc.temp', '/a/1.nc')

    def test_decreasing_exception_raised(self):
        """
        Test that an exception is raised if the file's latitude is increasing.
        """
        self.mock_lat_check.return_value = False
        fix = LatDirection('1.nc', '/a')
        self.assertRaisesRegex(ExistingAttributeError,
                               'Cannot edit attribute latitude in file 1.nc. '
                               'Latitude is not decreasing.', fix.apply_fix)

    def test_nco_errors_handled(self):
        """
        Test that errors in the nco commands to fix the bounds are handled.
        """
        fix = LatDirection('1.nc', '/a')
        self.mock_subprocess.side_effect = [
            None,
            None,
            None,
            None,
            RuntimeError('Not in the mood today')
        ]
        self.assertRaises(NcksError, fix.apply_fix)

    def test_temp_files_removed(self):
        self.mock_exists.return_value = True
        fix = LatDirection('1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call('/a/1.nc.temp'),
            mock.call('/a/1.nc'),
            mock.call('/a/1.nc.bnds'),
            mock.call('/a/1.nc.bnds_corr'),
            mock.call('/a/1.nc.bnds'),
            mock.call('/a/1.nc.bnds_corr')
        ]
        self.mock_remove.assert_has_calls(calls)


class TestLevToPlev(NcoDataFixBaseTest):
    """
    Test LevToPlev main functionality
    """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        LevToPlev
        """
        fix = LevToPlev('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_with(
            'ncrename -h -d lev,plev -v lev,plev /a/1.nc /a/1.nc.temp',
            stderr=subprocess.STDOUT, shell=True
        )


class TestLatDirectionLatitudeCheck(unittest.TestCase):
    """
    Test LatDirection._is_lat_decreasing()
    """
    def setUp(self):
        """ Mock loading a cube """
        patch = mock.patch('pre_proc.file_fix.data_fixes.iris.load_cube')
        mock_iris_load = patch.start()
        self.cube = realistic_3d()
        lat_coord = self.cube.coord('grid_latitude')
        lat_coord.standard_name = 'latitude'
        mock_iris_load.return_value = self.cube
        self.addCleanup(patch.stop)

    def test_direction_test_passes(self):
        """
        Check test passes for decreasing latitude.
        """
        fix = LatDirection('1.nc', '/a')
        # flip the latitude dimension
        self.cube.coord('latitude').points = np.flip(
            self.cube.coord('latitude').points
        )
        self.assertTrue(fix._is_lat_decreasing())

    def test_direction_test_fails(self):
        """
        Check test fails for increasing latitude.
        """
        fix = LatDirection('1.nc', '/a')
        self.assertFalse(fix._is_lat_decreasing())


class TestAAVarNameToFileName(NcoDataFixBaseTest):
    """
    Test AAVarNameToFileName main functionality
    """
    def setUp(self):
        """Patch call to Iris"""
        super().setUp()

        patch = mock.patch('pre_proc.file_fix.data_fixes.AAVarNameToFileName.'
                           '_get_existing_name')
        self.mock_iris = patch.start()
        self.mock_iris.return_value = 'hus7h'
        self.addCleanup(patch.stop)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        AAVarNameToFileName
        """
        fix = AAVarNameToFileName('hus_blah_blah.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call('ncrename -h -v hus7h,hus /a/hus_blah_blah.nc '
                      '/a/hus_blah_blah.nc.temp',
                      stderr=subprocess.STDOUT, shell=True),
            mock.call('ncatted -h -a variable_id,global,m,c,hus '
                      '/a/hus_blah_blah.nc /a/hus_blah_blah.nc.temp',
                      stderr=subprocess.STDOUT, shell=True)
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestToDegC(NcoDataFixBaseTest):
    """
    Test TosToDegC main functionality
    """
    def setUp(self):
        """ Use NcoDataFixBaseTest but also patch the unique external calls """
        super().setUp()

        patch = mock.patch('pre_proc.file_fix.data_fixes.ToDegC.'
                           '_is_kelvin')
        self.mock_kelvin_check = patch.start()
        self.mock_kelvin_check.return_value = True
        self.addCleanup(patch.stop)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        LatDirection
        """
        fix = ToDegC('tos_table.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call("ncap2 -h -s 'tos=tos-273.15f' /a/tos_table.nc "
                      "/a/tos_table.nc.temp",
                      stderr=subprocess.STDOUT, shell=True),
            mock.call("ncatted -h -a units,tos,m,c,'degC' /a/tos_table.nc",
                      stderr=subprocess.STDOUT, shell=True)
        ]
        self.mock_subprocess.assert_has_calls(calls)

    def test_remove_called_correctly(self):
        """
        Test that input files is removed.
        """
        fix = ToDegC('tos_table.nc', '/a')
        fix.apply_fix()
        self.mock_remove.assert_called_once_with('/a/tos_table.nc')

    def test_rename_called_correctly(self):
        """
        Test that output file is renamed.
        """
        fix = ToDegC('tos_table.nc', '/a')
        fix.apply_fix()
        self.mock_rename.assert_called_once_with('/a/tos_table.nc.temp',
                                                 '/a/tos_table.nc')

    def test_exception_raised(self):
        """
        Test that an exception is raised if the file's units are already degC.
        """
        self.mock_kelvin_check.return_value = False
        fix = ToDegC('tos_table.nc', '/a')
        self.assertRaisesRegex(ExistingAttributeError,
                               'Cannot edit attribute units in file '
                               'tos_table.nc. Units are not K.', fix.apply_fix)


class TestToDegCUnitsCheck(unittest.TestCase):
    """
    Test ToDegC._is_kelvin()
    """
    def setUp(self):
        """ Mock loading a cube """
        patch = mock.patch('pre_proc.file_fix.data_fixes.iris.load_cube')
        mock_iris_load = patch.start()
        self.cube = realistic_3d()
        mock_iris_load.return_value = self.cube
        self.addCleanup(patch.stop)

    def test_kelvin(self):
        """
        Check test passes for kelvin.
        """
        self.cube.units = cf_units.Unit('kelvin')
        fix = ToDegC('tos_table.nc', '/a')
        self.assertTrue(fix._is_kelvin())

    def test_fails(self):
        """
        Check test fails for degC.
        """
        self.cube.units = cf_units.Unit('degC')
        fix = ToDegC('tos_table.nc', '/a')
        self.assertFalse(fix._is_kelvin())


class TestZZEcEarthAtmosFix(unittest.TestCase):
    """
    Test ZZEcEarthAtmosFix
    """
    def setUp(self):
        patch = mock.patch('pre_proc.file_fix.data_fixes.fix_latlon_atmosphere')
        self.mock_fix = patch.start()
        self.addCleanup(patch.stop)

    def test_arguments(self):
        fix = ZZEcEarthAtmosFix('tas_table.nc', '/a')
        fix.apply_fix()
        self.mock_fix.assert_called_with('/a/tas_table.nc', 64 * 1024)


class TestZZZEcEarthLongitudeFix(unittest.TestCase):
    """
    Test ZZZEcEarthLongitudeFix
    """
    def setUp(self):
        patch = mock.patch('pre_proc.file_fix.data_fixes.fix_lons.fix_file')
        self.mock_fix = patch.start()
        self.addCleanup(patch.stop)

    def test_arguments(self):
        fix = ZZZEcEarthLongitudeFix('tas_table.nc', '/a')
        fix.apply_fix()
        self.mock_fix.assert_called_with('/a/tas_table.nc', write=True,
                                         keepid=True)


class TestSetTimeReference1949(NcoDataFixBaseTest):
    """
    Test SetTimeReference1949
    """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SetTimeReference1949
        """
        fix = SetTimeReference1949('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_with(
            "cdo -z zip_3 -setreftime,'1949-01-01','00:00:00' /a/1.nc "
            "/a/1.nc.temp",
            stderr=subprocess.STDOUT, shell=True
        )


class TestZZZAddHeight2m(NcoDataFixBaseTest):
    """
    Test ZZZAddHeight2m with some additional tests to check that
    NcksAppendDataFix works as intended.
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for ZZZAddHeight2m
        """
        fix = ZZZAddHeight2m('tas_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h -A -v height /gws/nopw/j04/primavera1/cache/jseddon/"
                "reference_files/height2m_reference.nc /a/tas_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncatted -h -a coordinates,tas,o,c,'height' /a/tas_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)

    def test_remove_called_correctly(self):
        """
        Test that input files is removed.
        """
        self.mock_exists.return_value = True
        fix = ZZZAddHeight2m('1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call('/a/1.nc.temp'),
            mock.call('/a/1.nc')
        ]
        self.mock_remove.assert_has_calls(calls)

    def test_rename_called_correctly(self):
        """
        Test that output file is renamed.
        """
        fix = ZZZAddHeight2m('1.nc', '/a')
        fix.apply_fix()
        self.mock_rename.assert_called_once_with('/a/1.nc.temp', '/a/1.nc')


class TestRemoveOrca1Halo(NcoDataFixBaseTest):
    """
    Test RemoveOrca1Halo
    """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RemoveOrca1Halo
        """
        fix = AAARemoveOrca1Halo('tas_1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_with(
            "ncks -h --no_alphabetize -di,1,360 -dj,1,330 /a/tas_1.nc "
            "/a/tas_1.nc.temp",
            stderr=subprocess.STDOUT, shell=True
        )


class TestRemoveOrca025Halo(NcoDataFixBaseTest):
    """
    Test RemoveOrca025Halo
    """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RemoveOrca025Halo
        """
        fix = AAARemoveOrca025Halo('tas_1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_with(
            "ncks -h --no_alphabetize -di,1,1440 -dj,1,1205 /a/tas_1.nc "
            "/a/tas_1.nc.temp",
            stderr=subprocess.STDOUT, shell=True
        )


class TestMaskOrca1TOlevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1TOlevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca1TOlevel
        """
        fix = FixMaskOrca1TOlevel('tos_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_T "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/primavera_byte_masks.nc "
                "/a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_T != 0) tos=tos@_FillValue' "
                "/a/tos_1.nc.temp /a/tos_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_T "
                "/a/tos_1.nc.temp_masked /a/tos_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025TOlevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025TOlevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca025TOlevel
        """
        fix = FixMaskOrca025TOlevel('tos_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_T "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/primavera_byte_masks.nc "
                "/a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_T != 0) tos=tos@_FillValue' "
                "/a/tos_1.nc.temp /a/tos_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_T "
                "/a/tos_1.nc.temp_masked /a/tos_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1UOlevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1UOlevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca1UOlevel
        """
        fix = FixMaskOrca1UOlevel('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_U "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/primavera_byte_masks.nc "
                "/a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_U != 0) uo=uo@_FillValue' "
                "/a/uo_1.nc.temp /a/uo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_U "
                "/a/uo_1.nc.temp_masked /a/uo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025UOlevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025UOlevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca025UOlevel
        """
        fix = FixMaskOrca025UOlevel('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_U "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/primavera_byte_masks.nc "
                "/a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_U != 0) uo=uo@_FillValue' "
                "/a/uo_1.nc.temp /a/uo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_U "
                "/a/uo_1.nc.temp_masked /a/uo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1VOlevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1VOlevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca1VOlevel
        """
        fix = FixMaskOrca1VOlevel('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_V "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/primavera_byte_masks.nc "
                "/a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_V != 0) vo=vo@_FillValue' "
                "/a/vo_1.nc.temp /a/vo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_V "
                "/a/vo_1.nc.temp_masked /a/vo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025VOlevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025VOlevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca025VOlevel
        """
        fix = FixMaskOrca025VOlevel('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_V "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/primavera_byte_masks.nc "
                "/a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_V != 0) vo=vo@_FillValue' "
                "/a/vo_1.nc.temp /a/vo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_V "
                "/a/vo_1.nc.temp_masked /a/vo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1TSurface(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1TSurface
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca1TSurface
        """
        fix = FixMaskOrca1TSurface('tos_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_2D_T "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/primavera_byte_masks.nc "
                "/a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_2D_T != 0) tos=tos@_FillValue' "
                "/a/tos_1.nc.temp /a/tos_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_2D_T "
                "/a/tos_1.nc.temp_masked /a/tos_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025TSurface(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025TSurface
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca025TSurface
        """
        fix = FixMaskOrca025TSurface('tos_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_2D_T "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/primavera_byte_masks.nc "
                "/a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_2D_T != 0) tos=tos@_FillValue' "
                "/a/tos_1.nc.temp /a/tos_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_2D_T "
                "/a/tos_1.nc.temp_masked /a/tos_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1USurface(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1USurface
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca1USurface
        """
        fix = FixMaskOrca1USurface('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_2D_U "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/primavera_byte_masks.nc "
                "/a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_2D_U != 0) uo=uo@_FillValue' "
                "/a/uo_1.nc.temp /a/uo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_2D_U "
                "/a/uo_1.nc.temp_masked /a/uo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1USingleLevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1USingleLevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for
        FixMaskOrca1USingleLevel
        """
        fix = FixMaskOrca1USingleLevel('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_U "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/"
                "primavera_single_level_byte_masks.nc "
                "/a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_U != 0) uo=uo@_FillValue' "
                "/a/uo_1.nc.temp /a/uo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_U "
                "/a/uo_1.nc.temp_masked /a/uo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025USurface(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025USurface
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca025USurface
        """
        fix = FixMaskOrca025USurface('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_2D_U "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/primavera_byte_masks.nc "
                "/a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_2D_U != 0) uo=uo@_FillValue' "
                "/a/uo_1.nc.temp /a/uo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_2D_U "
                "/a/uo_1.nc.temp_masked /a/uo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025USingleLevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025USingleLevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for
        FixMaskOrca025USingleLevel
        """
        fix = FixMaskOrca025USingleLevel('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_U "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/"
                "primavera_single_level_byte_masks.nc "
                "/a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_U != 0) uo=uo@_FillValue' "
                "/a/uo_1.nc.temp /a/uo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_U "
                "/a/uo_1.nc.temp_masked /a/uo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1VSurface(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1VSurface
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca1VSurface
        """
        fix = FixMaskOrca1VSurface('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_2D_V "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/primavera_byte_masks.nc "
                "/a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_2D_V != 0) vo=vo@_FillValue' "
                "/a/vo_1.nc.temp /a/vo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_2D_V "
                "/a/vo_1.nc.temp_masked /a/vo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca1VSingleLevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca1VSingleLevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for
        FixMaskOrca1VSingleLevel
        """
        fix = FixMaskOrca1VSingleLevel('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_V "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-LL/"
                "primavera_single_level_byte_masks.nc "
                "/a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_V != 0) vo=vo@_FillValue' "
                "/a/vo_1.nc.temp /a/vo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_V "
                "/a/vo_1.nc.temp_masked /a/vo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025VSurface(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025VSurface
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixMaskOrca025VSurface
        """
        fix = FixMaskOrca025VSurface('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_2D_V "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/primavera_byte_masks.nc "
                "/a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_2D_V != 0) vo=vo@_FillValue' "
                "/a/vo_1.nc.temp /a/vo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_2D_V "
                "/a/vo_1.nc.temp_masked /a/vo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestMaskOrca025VSingleLevel(NcoDataFixBaseTest):
    """
    Test FixMaskOrca025VSingleLevel
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for
        FixMaskOrca025VSingleLevel
        """
        fix = FixMaskOrca025VSingleLevel('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -A -v mask_3D_V "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "bytes_masks/HadGEM3-GC31-MM/"
                "primavera_single_level_byte_masks.nc "
                "/a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncap2 -h -s 'where(mask_3D_V != 0) vo=vo@_FillValue' "
                "/a/vo_1.nc.temp /a/vo_1.nc.temp_masked",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -x -v mask_3D_V "
                "/a/vo_1.nc.temp_masked /a/vo_1.nc.temp_final",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixGridOrca1T(NcoDataFixBaseTest):
    """
    Test FixGridOrca1T
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixGridOrca1T
        """
        fix = FixGridOrca1T('tos_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/tos_1.nc /a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "grids/ORCA1/ORCA1_grid-t.nc /a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/tos_1.nc.temp "
                "/a/tos_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixGridOrca025T(NcoDataFixBaseTest):
    """
    Test FixGridOrca025T
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixGridOrca025T
        """
        fix = FixGridOrca025T('tos_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/tos_1.nc /a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "grids/ORCA025/ORCA025_grid-t.nc /a/tos_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/tos_1.nc.temp "
                "/a/tos_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixGridOrca1U(NcoDataFixBaseTest):
    """
    Test FixGridOrca1U
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixGridOrca1U
        """
        fix = FixGridOrca1U('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/uo_1.nc /a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "grids/ORCA1/ORCA1_grid-u.nc /a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/uo_1.nc.temp "
                "/a/uo_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixGridOrca025U(NcoDataFixBaseTest):
    """
    Test FixGridOrca025U
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixGridOrca025U
        """
        fix = FixGridOrca025U('uo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/uo_1.nc /a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "grids/ORCA025/ORCA025_grid-u.nc /a/uo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/uo_1.nc.temp "
                "/a/uo_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixGridOrca1V(NcoDataFixBaseTest):
    """
    Test FixGridOrca1V
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixGridOrca1V
        """
        fix = FixGridOrca1V('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/vo_1.nc /a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "grids/ORCA1/ORCA1_grid-v.nc /a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/vo_1.nc.temp "
                "/a/vo_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixGridOrca025V(NcoDataFixBaseTest):
    """
    Test FixGridOrca025V
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixGridOrca025V
        """
        fix = FixGridOrca025V('vo_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/vo_1.nc /a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/"
                "grids/ORCA025/ORCA025_grid-v.nc /a/vo_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/vo_1.nc.temp "
                "/a/vo_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixCiceCoords1T(NcoDataFixBaseTest):
    """
    Test FixCiceCoords1T
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixCiceCoords1T
        """
        fix = FixCiceCoords1T('siconc_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/siconc_1.nc "
                "/a/siconc_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/cice_coords/"
                "eORCA1/cice_eORCA1_coords_grid-t.nc /a/siconc_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/siconc_1.nc.temp "
                "/a/siconc_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)


class TestFixCiceCoords1UV(NcoDataFixBaseTest):
    """
    Test FixCiceCoords1UV
    """
    def test_subprocess_called_correctly(self):
        """
        Test that external calls are made correctly for FixCiceCoords1UV
        """
        fix = FixCiceCoords1UV('siv_1.nc', '/a')
        fix.apply_fix()
        calls = [
            mock.call(
                "ncks -h --no_alphabetize -3 /a/siv_1.nc "
                "/a/siv_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -A -v latitude,longitude,"
                "vertices_latitude,vertices_longitude "
                "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/cice_coords/"
                "eORCA1/cice_eORCA1_coords_grid-uv.nc /a/siv_1.nc.temp",
                stderr=subprocess.STDOUT, shell=True
            ),
            mock.call(
                "ncks -h --no_alphabetize -7 --deflate=3 /a/siv_1.nc.temp "
                "/a/siv_1.nc",
                stderr=subprocess.STDOUT, shell=True
            ),
        ]
        self.mock_subprocess.assert_has_calls(calls)
