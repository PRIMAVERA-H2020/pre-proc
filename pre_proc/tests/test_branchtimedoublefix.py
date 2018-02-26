"""
test_branchtimedoublefix.py

Unit tests for all BranchTimeDoubleFix classes from file_fix.py
"""
import subprocess
import unittest

import mock

from pre_proc.exceptions import (AttributeNotFoundError,
                                 AttributeConversionError)
from pre_proc.file_fix import (ParentBranchTimeDoubleFix,
                               ChildBranchTimeDoubleFix)


class TestStarBranchTimeDoubleFix(unittest.TestCase):
    """ Test all BranchTimeDoubleFix classes """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)

        class MockedNamespace(object):
            branch_time_in_child = "0.0"
            branch_time_in_parent = "1080.0"

            def __exit__(self, *args):
                pass

            def __enter__(self):
                return self

        patch = mock.patch('pre_proc.file_fix.Dataset')
        self.mock_dataset = patch.start()
        self.mock_dataset.return_value = MockedNamespace()
        self.addCleanup(patch.stop)

    def test_no_attribute(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = ParentBranchTimeDoubleFix(['1.nc'], '/a', '/b')
        fix.attribute_name = 'not_present'
        self.assertRaises(AttributeNotFoundError, fix.apply_fix)

    def test_wrong_attribute_type(self):
        """ Test if the required attribute can't be converted """
        fix = ParentBranchTimeDoubleFix(['1.nc'], '/a', '/b')
        self.mock_dataset.return_value.branch_time_in_parent = 'wrong_type'
        self.assertRaises(AttributeConversionError, fix.apply_fix)

    def test_subprocess_called_correctly_parent(self):
        """ Test that an external call's been made """
        fix = ParentBranchTimeDoubleFix(['1.nc'], '/a', '/b')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_parent,global,o,d,1080.0 '
            '/a/1.nc /b/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_subprocess_called_correctly_child(self):
        """ Test that an external call's been made """
        fix = ChildBranchTimeDoubleFix(['1.nc'], '/a', '/b')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_child,global,o,d,0.0 '
            '/a/1.nc /b/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_two_files(self):
        """ Check that all files in a directory are fixed """
        fix = ChildBranchTimeDoubleFix(['1.nc', '2.nc'], '/a', '/b')
        fix.apply_fix()
        self.mock_subprocess.assert_any_call(
            'ncatted -h -a branch_time_in_child,global,o,d,0.0 '
            '/a/1.nc /b/1.nc',
            stderr=subprocess.STDOUT,
            shell=True)
        self.mock_subprocess.assert_any_call(
            'ncatted -h -a branch_time_in_child,global,o,d,0.0 '
            '/a/2.nc /b/2.nc',
            stderr=subprocess.STDOUT,
            shell=True)
        self.assertEqual(self.mock_subprocess.call_count, 2)


if __name__ == '__main__':
    unittest.main()
