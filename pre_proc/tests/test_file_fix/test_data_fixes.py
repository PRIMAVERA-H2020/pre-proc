"""
test_data_fixes.py

Unit tests for all FileFix concrete classes from data_fixes.py
"""
import subprocess
import unittest
from unittest import mock

from iris.tests.stock import realistic_3d
import numpy as np

from pre_proc.exceptions import ExistingAttributeError
from pre_proc.file_fix import LatDirection


class BaseTest(unittest.TestCase):
    """ Base class to setup a typical environment used by other tests """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)


class TestLatDirection(BaseTest):
    """ Test LatDirection main functionality """
    def setUp(self):
        """ Use BaseTest but also patch two external calls """
        super().setUp()

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.remove')
        self.mock_remove = patch.start()
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.rename')
        self.mock_rename = patch.start()
        self.addCleanup(patch.stop)

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
        self.mock_subprocess.assert_called_once_with(
            'ncpdq -a -lat /a/1.nc /a/1.nc.temp',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_remove_called_correctly(self):
        """
        Test that input files is removed.
        """
        fix = LatDirection('1.nc', '/a')
        fix.apply_fix()
        self.mock_remove.assert_called_once_with('/a/1.nc')

    def test_rename_called_correctly(self):
        """
        Test that output file is renamed.
        """
        fix = LatDirection('1.nc', '/a')
        fix.apply_fix()
        self.mock_rename.assert_called_once_with('/a/1.nc.temp', '/a/1.nc')

    def test_exception_raised(self):
        """
        Test that an exception is raised if the file's latitude is increasing.
        """
        self.mock_lat_check.return_value = True
        fix = LatDirection('1.nc', '/a')
        self.assertRaisesRegex(ExistingAttributeError,
                               'Cannot edit attribute latitude in file 1.nc. '
                               'Latitude is not decreasing.', fix.apply_fix)


class TestLatDirectionLatitudeCheck(BaseTest):
    """ Test LatDirection._is_lat_decreasing() """
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
        Check test fails for decreasing latitude.
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
