"""
test_branchtimedoublefix.py

Unit tests for all BranchTimeDoubleFix classes from file_fix.py
"""
import subprocess
import unittest

import mock

from pre_proc.exceptions import (AttributeNotFoundError,
                                 AttributeConversionError,
                                 AttributeEditError)
from pre_proc.file_fix import (ParentBranchTimeDoubleFix,
                               ChildBranchTimeDoubleFix,
                               FurtherInfoUrlToHttps)


class TestAttEdFix(unittest.TestCase):
    """ Test all AttEdFix child classes """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)

        class MockedNamespace(object):
            branch_time_in_child = '0.0'
            branch_time_in_parent = '1080.0'
            further_info_url = 'http://furtherinfo.es-doc.org/part1.part2'

            def __exit__(self, *args):
                pass

            def __enter__(self):
                return self

        patch = mock.patch('pre_proc.file_fix.Dataset')
        self.mock_dataset = patch.start()
        self.mock_dataset.return_value = MockedNamespace()
        self.addCleanup(patch.stop)

    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        fix.attribute_name = 'not_present'
        exception_text = ('Cannot find attribute not_present in file 1.nc')
        self.assertRaisesRegexp(AttributeNotFoundError, exception_text,
                                fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        self.mock_dataset.return_value.branch_time_in_parent = 'pure_text'
        exception_text = ('Cannot convert attribute branch_time_in_parent to '
                          'new type float in file 1.nc')
        self.assertRaisesRegexp(AttributeConversionError, exception_text,
                                fix.apply_fix)

    def test_subprocess_called_correctly_parent(self):
        """
        Test that an external call's been made correctly for
        ParentBranchTimeDoubleFix
        """
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_parent,global,o,d,1080.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_subprocess_called_correctly_child(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeDoubleFix
        """
        fix = ChildBranchTimeDoubleFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_child,global,o,d,0.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_subprocess_called_correctly_further_info_url(self):
        """
        Test that an external call's been made correctly for
        FurtherInfoUrlToHttps
        """
        fix = FurtherInfoUrlToHttps('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a further_info_url,global,o,m,"
            "'https://furtherinfo.es-doc.org/part1.part2' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_further_info_url_raises_if_https(self):
        """
        Test that an external call's been made correctly for
        FurtherInfoUrlToHttps
        """
        fix = FurtherInfoUrlToHttps('1.nc', '/a')
        self.mock_dataset.return_value.further_info_url = 'https://a.url/'
        exception_text = ('Cannot edit attribute further_info_url in file '
                          '1.nc. Existing further_info_url attribute does not '
                          'start with http:')
        self.assertRaisesRegexp(AttributeEditError, exception_text,
                                fix.apply_fix)


if __name__ == '__main__':
    unittest.main()
