"""
test_data_fixes.py

Unit tests for all FileFix concrete classes from data_fixes.py
"""
import subprocess
import unittest

import mock

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
    """ Test LatDirection """
    def setUp(self):
        """ Use BaseTest but also patch two external calls """
        super().setUp()

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.remove')
        self.mock_remove = patch.start()
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.data_fixes.os.rename')
        self.mock_rename = patch.start()
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
