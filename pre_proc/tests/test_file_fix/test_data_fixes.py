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
from pre_proc.file_fix import LatDirection, ToDegC


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
