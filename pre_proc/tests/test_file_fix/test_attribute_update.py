"""
test_attribute_add.py

Unit tests for all FileFix concrete classes from attribute_add.py
"""
import subprocess
import unittest

import mock

from pre_proc.exceptions import (AttributeNotFoundError,
                                 AttributeConversionError,
                                 ExistingAttributeError,
                                 InstanceVariableNotDefinedError)
from pre_proc.file_fix import (ParentBranchTimeDoubleFix,
                               ChildBranchTimeDoubleFix,
                               ForcingIndexIntFix,
                               InitializationIndexIntFix,
                               PhysicsIndexIntFix,
                               RealizationIndexIntFix,
                               FurtherInfoUrlToHttps,
                               FurtherInfoUrlAWISourceIdAndHttps,
                               FurtherInfoUrlPrimToHttps,
                               AogcmToAgcm, TrackingIdFix)


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

        self.dataset = MockedNamespace()

        patch = mock.patch('pre_proc.file_fix.abstract.Dataset')
        self.mock_dataset = patch.start()
        self.mock_dataset.return_value = self.dataset
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.file_fix.attribute_update.Dataset')
        self.mock_local_dataset = patch.start()
        self.mock_local_dataset.return_value = self.dataset
        self.addCleanup(patch.stop)


class TestParentBranchTimeDoubleFix(BaseTest):
    """ Test ParentBranchTimeDoubleFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        exception_text = ('Cannot find attribute branch_time_in_parent in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        self.mock_dataset.return_value.branch_time_in_parent = 'pure_text'
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        exception_text = ('Cannot convert attribute branch_time_in_parent to '
                          'new type float in file 1.nc')
        self.assertRaisesRegex(AttributeConversionError, exception_text,
                               fix.apply_fix)

    def test_no_attribute_name_raises(self):
        """ Test whether missing attribute_name handled """
        self.mock_dataset.return_value.branch_time_in_parent = '1080.0'
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        exception_text = ('ParentBranchTimeDoubleFix: attribute '
                          'attribute_name is not defined')
        fix._get_existing_value()
        fix._calculate_new_value()
        fix.attribute_name = None
        self.assertRaisesRegex(InstanceVariableNotDefinedError,
                               exception_text, fix._run_ncatted, 'o')

    def test_no_visibility_raises(self):
        """ Test whether missing visibility handled """
        self.mock_dataset.return_value.branch_time_in_parent = '1080.0'
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        fix.attribute_visibility = None
        exception_text = ('ParentBranchTimeDoubleFix: attribute '
                          'attribute_visibility is not defined')
        self.assertRaisesRegex(InstanceVariableNotDefinedError,
                               exception_text, fix.apply_fix)

    def test_no_new_value_raises(self):
        """ Test whether missing new_value handled """
        self.mock_dataset.return_value.branch_time_in_parent = '1080.0'
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        exception_text = ('ParentBranchTimeDoubleFix: attribute '
                          'new_value is not defined')
        fix._get_existing_value()
        fix._calculate_new_value()
        fix.new_value = None
        self.assertRaisesRegex(InstanceVariableNotDefinedError,
                               exception_text, fix._run_ncatted, 'o')

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ParentBranchTimeDoubleFix
        """
        self.mock_dataset.return_value.branch_time_in_parent = '1080.0'
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_parent,global,o,d,1080.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )

    def test_subprocess_called_correctly_with_trailing_letter(self):
        """
        Test that an external call's been made correctly for
        ParentBranchTimeDoubleFix when there is a trailing letter
        """
        self.mock_dataset.return_value.branch_time_in_parent = '0.0D'
        fix = ParentBranchTimeDoubleFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_parent,global,o,d,0.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestChildBranchTimeDoubleFix(BaseTest):
    """ Test ChildBranchTimeDoubleFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = ChildBranchTimeDoubleFix('1.nc', '/a')
        exception_text = ('Cannot find attribute branch_time_in_child in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        self.mock_dataset.return_value.branch_time_in_child = 'pure_text'
        fix = ChildBranchTimeDoubleFix('1.nc', '/a')
        exception_text = ('Cannot convert attribute branch_time_in_child to '
                          'new type float in file 1.nc')
        self.assertRaisesRegex(AttributeConversionError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeDoubleFix
        """
        self.mock_dataset.return_value.branch_time_in_child = '0.0'
        fix = ChildBranchTimeDoubleFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_child,global,o,d,0.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestInitializationIndexIntFix(BaseTest):
    """ Test InitializationIndexIntFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = InitializationIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot find attribute initialization_index in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        self.mock_dataset.return_value.initialization_index = 'pure_text'
        fix = InitializationIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot convert attribute initialization_index to '
                          'new type int in file 1.nc')
        self.assertRaisesRegex(AttributeConversionError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        InitializationIndexIntFix
        """
        self.mock_dataset.return_value.initialization_index = '99'
        fix = InitializationIndexIntFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a initialization_index,global,o,s,99 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestForcingIndexIntFix(BaseTest):
    """ Test ForcingIndexIntFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = ForcingIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot find attribute forcing_index in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        self.mock_dataset.return_value.forcing_index = 'pure_text'
        fix = ForcingIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot convert attribute forcing_index to '
                          'new type int in file 1.nc')
        self.assertRaisesRegex(AttributeConversionError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ForcingIndexIntFix
        """
        self.mock_dataset.return_value.forcing_index = '99'
        fix = ForcingIndexIntFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a forcing_index,global,o,s,99 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestPhysicsIndexIntFix(BaseTest):
    """ Test PhysicsIndexIntFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = PhysicsIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot find attribute physics_index in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        self.mock_dataset.return_value.physics_index = 'pure_text'
        fix = PhysicsIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot convert attribute physics_index to '
                          'new type int in file 1.nc')
        self.assertRaisesRegex(AttributeConversionError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        PhysicsIndexIntFix
        """
        self.mock_dataset.return_value.physics_index = '99'
        fix = PhysicsIndexIntFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a physics_index,global,o,s,99 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestRealizationIndexIntFix(BaseTest):
    """ Test RealizationIndexIntFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = RealizationIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot find attribute realization_index in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_wrong_attribute_type_raises(self):
        """ Test if the required attribute can't be converted """
        self.mock_dataset.return_value.realization_index = 'pure_text'
        fix = RealizationIndexIntFix('1.nc', '/a')
        exception_text = ('Cannot convert attribute realization_index to '
                          'new type int in file 1.nc')
        self.assertRaisesRegex(AttributeConversionError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RealizationIndexIntFix
        """
        self.mock_dataset.return_value.realization_index = '99'
        fix = RealizationIndexIntFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a realization_index,global,o,s,99 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestFurtherInfoUrlToHttps(BaseTest):
    """ Test FurtherInfoUrlToHttps """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = FurtherInfoUrlToHttps('1.nc', '/a')
        exception_text = ('Cannot find attribute further_info_url in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_not_http(self):
        """ Test exception is raised if it doesn't start with http """
        self.mock_dataset.return_value.further_info_url = 'https://a.url/'
        fix = FurtherInfoUrlToHttps('1.nc', '/a')
        exception_text = ('Existing further_info_url attribute does not start '
                          'with http:')
        self.assertRaisesRegex(ExistingAttributeError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly_further_info_url(self):
        """
        Test that an external call's been made correctly for
        FurtherInfoUrlToHttps
        """
        self.mock_dataset.return_value.further_info_url = (
            'http://furtherinfo.es-doc.org/part1.part2'
        )
        fix = FurtherInfoUrlToHttps('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a further_info_url,global,o,c,"
            "'https://furtherinfo.es-doc.org/part1.part2' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestFurtherInfoUrlAWISourceIdAndHttps(BaseTest):
    """ Test FurtherInfoUrlAWISourceIdAndHttps """
    def test_no_further_info_raises(self):
        """ Test whether missing further_info_url handled """
        self.mock_dataset.return_value.source_id = 'AWI-CM-1-0-LR'
        fix = FurtherInfoUrlAWISourceIdAndHttps('1.nc', '/a')
        exception_text = ('Cannot find attribute further_info_url in file '
                          '1.nc')
        self.assertRaisesRegex(AttributeNotFoundError,
                               exception_text, fix._get_existing_value)

    def test_no_source_id_raises(self):
        """ Test whether missing source_id handled """
        self.mock_dataset.return_value.further_info_url = (
            'http://furtherinfo.es-doc.org/CMIP6.AWI.AWI-CM-1-0.hist-1950.'
            'none.r1i1p1f002'
        )
        fix = FurtherInfoUrlAWISourceIdAndHttps('1.nc', '/a')
        exception_text = ('Cannot find attribute source_id in file '
                          '1.nc')
        self.assertRaisesRegex(AttributeNotFoundError,
                               exception_text, fix._get_existing_value)

    def test_wrong_existing_value_raises(self):
        """ Test whether invalid existing_value handled """
        self.mock_dataset.return_value.further_info_url = 'apples'
        self.mock_dataset.return_value.source_id = 'pairs'
        fix = FurtherInfoUrlAWISourceIdAndHttps('1.nc', '/a')
        exception_text = ('Cannot edit attribute further_info_url in file '
                          '1.nc. Existing further_info_url attribute '
                          'does not start with http:')
        fix._get_existing_value()
        self.assertRaisesRegex(ExistingAttributeError,
                               exception_text, fix._calculate_new_value)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        FurtherInfoUrlAWISourceIdAndHttps
        """
        self.mock_dataset.return_value.source_id = 'AWI-CM-1-0-LR'
        self.mock_dataset.return_value.further_info_url = (
            'http://furtherinfo.es-doc.org/CMIP6.AWI.AWI-CM-1-0.hist-1950.'
            'none.r1i1p1f002'
        )
        fix = FurtherInfoUrlAWISourceIdAndHttps('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a further_info_url,global,o,c,"
            "'https://furtherinfo.es-doc.org/CMIP6.AWI.AWI-CM-1-0-LR."
            "hist-1950.none.r1i1p1f002' /a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestFurtherInfoUrlPrimToHttps(BaseTest):
    """ Test FurtherInfoUrlPrimToHttps """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = FurtherInfoUrlPrimToHttps('1.nc', '/a')
        exception_text = ('Cannot find attribute further_info_url in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_not_http(self):
        """ Test exception is raised if it doesn't start with http """
        self.mock_dataset.return_value.further_info_url = 'https://a.url/'
        fix = FurtherInfoUrlPrimToHttps('1.nc', '/a')
        exception_text = ('Existing further_info_url attribute does not start '
                          'with http://furtherinfo.es-doc.org/CMIP6')
        self.assertRaisesRegex(ExistingAttributeError, exception_text,
                               fix.apply_fix)

    def test_not_cmip6(self):
        """ Test exception is raised if it isn't CMIP6 """
        self.mock_dataset.return_value.further_info_url = (
            'http://furtherinfo.es-doc.org/CORDEX'
        )
        fix = FurtherInfoUrlPrimToHttps('1.nc', '/a')
        exception_text = ('Existing further_info_url attribute does not start '
                          'with http://furtherinfo.es-doc.org/CMIP6')
        self.assertRaisesRegex(ExistingAttributeError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly_further_info_url(self):
        """
        Test that an external call's been made correctly for
        FurtherInfoUrlPrimToHttps
        """
        self.mock_dataset.return_value.further_info_url = (
            'http://furtherinfo.es-doc.org/CMIP6.part2'
        )
        fix = FurtherInfoUrlPrimToHttps('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a further_info_url,global,o,c,"
            "'https://furtherinfo.es-doc.org/PRIMAVERA.part2' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestAogcmToAgcm(BaseTest):
    """ Test AogcmToAgcm """
    def test_agcm_raises(self):
        """ Test whether missing further_info_url handled """
        self.mock_dataset.return_value.source_type = 'AGCM'
        fix = AogcmToAgcm('1.nc', '/a')
        exception_text = ('Cannot edit attribute source_type in file '
                          '1.nc. Existing value is not AOGCM.')
        fix._get_existing_value()
        self.assertRaisesRegex(ExistingAttributeError,
                               exception_text, fix._calculate_new_value)

    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        AogcmToAgcm
        """
        self.mock_dataset.return_value.source_type = 'AOGCM'
        fix = AogcmToAgcm('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a source_type,global,o,c,"
            "'AGCM' /a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestTrackingIdFix(BaseTest):
    """ Test TrackingIdFix """
    def test_no_attribute_raises(self):
        """ Test if the required attribute isn't found in the netCDF """
        fix = TrackingIdFix('1.nc', '/a')
        exception_text = ('Cannot find attribute tracking_id in '
                          'file 1.nc')
        self.assertRaisesRegex(AttributeNotFoundError, exception_text,
                               fix.apply_fix)

    def test_not_hdl(self):
        """ Test exception is raised if it starts with hdl: """
        self.mock_dataset.return_value.tracking_id = 'hdl:/uuid'
        fix = TrackingIdFix('1.nc', '/a')
        exception_text = ('Existing tracking_id attribute starts with hdl:')
        self.assertRaisesRegex(ExistingAttributeError, exception_text,
                               fix.apply_fix)

    def test_subprocess_called_correctly_further_info_url(self):
        """
        Test that an external call's been made correctly for
        TrackingIdFix
        """
        self.mock_dataset.return_value.tracking_id = (
            '79fa5ac0-14cb-4a9f-bcff-ca097ba45c46'
        )
        fix = TrackingIdFix('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a tracking_id,global,o,c,"
            "'hdl:21.14100/79fa5ac0-14cb-4a9f-bcff-ca097ba45c46' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


if __name__ == '__main__':
    unittest.main()
