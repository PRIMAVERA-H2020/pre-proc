"""
test_attribute_add.py

Unit tests for all FileFix concrete classes from attribute_add.py
"""
import subprocess
import unittest

import mock

from pre_proc.exceptions import AttributeNotFoundError
from pre_proc.file_fix import (ParentSourceIdFromSourceId,
                               FillValueFromMissingValue)


class BaseTest(unittest.TestCase):
    """ Base class to setup a typical environment used by other tests """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)

        class MockedNamespace(object):
            def __exit__(self, *args):
                pass

            def __enter__(self):
                return self

        patch = mock.patch('pre_proc.file_fix.abstract.Dataset')
        self.mock_dataset = patch.start()
        self.mock_dataset.return_value = MockedNamespace()
        self.addCleanup(patch.stop)


class TestParentSourceIdFromSourceId(BaseTest):
    """ Test ParentSourceIdFromSourceId """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = ParentSourceIdFromSourceId('1.nc', '/a')
        exception_text = ('Cannot find attribute source_id in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ParentSourceIdFromSourceId
        """
        self.mock_dataset.return_value.source_id = 'some-model'
        self.mock_dataset.return_value.parent_source_id = 'a-model'
        fix = ParentSourceIdFromSourceId('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a parent_source_id,global,o,c,'some-model' /a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestFillValueFromMissingValue(BaseTest):
    """ Test FillValueFromMissingValue """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = FillValueFromMissingValue('tos_blah.nc', '/a')
        exception_text = ('Cannot find attribute tos.missing_value in '
                          'file tos_blah.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        FillValueFromMissingValue
        """
        class MissingValue(object):
            missing_value = 1e-7
        self.mock_dataset.return_value.variables = {'tos': MissingValue()}
        fix = FillValueFromMissingValue('tos_gubbins.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a _FillValue,tos,o,f,1e-07 /a/tos_gubbins.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


if __name__ == '__main__':
    unittest.main()
