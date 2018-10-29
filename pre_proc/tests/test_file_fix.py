"""
test_file_fix.py

Unit tests for all FileFix concrete classes from file_fix.py
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
                               FurtherInfoUrlToHttps,
                               ParentSourceIdFromSourceId,
                               ParentBranchTimeAdd,
                               ChildBranchTimeAdd,
                               BranchMethodAdd,
                               DataSpecsVersionAdd,
                               CellMeasuresAreacellaAdd,
                               CellMethodsAreaTimeMeanAdd,
                               InitializationIndexIntFix,
                               ForcingIndexIntFix,
                               PhysicsIndexIntFix,
                               RealizationIndexIntFix,
                               SeaWaterSalinityStandardNameAdd,
                               CellMethodsSeaAreaTimeMeanAdd,
                               CellMeasuresAreacelloVolcelloAdd,
                               VarUnitsToThousandths,
                               FurtherInfoUrlAWISourceIdAndHttps,
                               SeaSurfaceTemperatureNameAdd,
                               FillValueFromMissingValue,
                               CellMeasuresAreacelloAdd)


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

        patch = mock.patch('pre_proc.file_fix.Dataset')
        self.mock_dataset = patch.start()
        self.mock_dataset.return_value = MockedNamespace()
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
                                exception_text, fix._run_ncatted)

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
                                exception_text, fix._run_ncatted)

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


class TestParentBranchTimeAdd(BaseTest):
    """ Test ParentBranchTimeAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ParentBranchTimeAdd
        """
        fix = ParentBranchTimeAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_parent,global,o,d,0.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestChildBranchTimeAdd(BaseTest):
    """ Test ChildBranchTimeAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeAdd
        """
        fix = ChildBranchTimeAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            'ncatted -h -a branch_time_in_child,global,o,d,0.0 '
            '/a/1.nc',
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestBranchMethodAdd(BaseTest):
    """ Test BranchMethodAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeAdd
        """
        fix = BranchMethodAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a branch_method,global,o,c,'no parent' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDataSpecsVersionAdd(BaseTest):
    """ Test DataSpecsVersion """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeAdd
        """
        fix = DataSpecsVersionAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a data_specs_version,global,o,c,'01.00.23' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMeasuresAreacellaAdd(BaseTest):
    """ Test CellMeasuresAreacellaAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMeasuresAreacellaAdd
        """
        fix = CellMeasuresAreacellaAdd('tas_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_measures,tas,o,c,'area: areacella' "
            "/a/tas_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMeasuresAreacelloAdd(BaseTest):
    """ Test CellMeasuresAreacelloAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMeasuresAreacelloAdd
        """
        fix = CellMeasuresAreacelloAdd('tos_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_measures,tos,o,c,'area: areacello' "
            "/a/tos_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMeasuresAreacelloVolcelloAdd(BaseTest):
    """ Test CellMeasuresAreacelloVolcelloAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMeasuresAreacelloVolcelloAdd
        """
        fix = CellMeasuresAreacelloVolcelloAdd('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_measures,so,o,c,"
            "'area: areacello volume: volcello' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaTimeMeanAdd(BaseTest):
    """ Test CellMethodsAreaTimeMeanAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaTimeMeanAdd
        """
        fix = CellMethodsAreaTimeMeanAdd('tas_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,tas,o,c,'area: time: mean' "
            "/a/tas_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsSeaAreaTimeMeanAdd(BaseTest):
    """ Test CellMethodsSeaAreaTimeMeanAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsSeaAreaTimeMeanAdd
        """
        fix = CellMethodsSeaAreaTimeMeanAdd('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,so,o,c,"
            "'area: mean where sea time: mean' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSeaWaterSalinityStandardNameAdd(BaseTest):
    """ Test SeaWaterSalinityStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SeaWaterSalinityStandardNameAdd
        """
        fix = SeaWaterSalinityStandardNameAdd('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,so,o,c,'sea_water_salinity' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSeaSurfaceTemperatureNameAdd(BaseTest):
    """ Test SeaSurfaceTemperatureNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SeaSurfaceTemperatureNameAdd
        """
        fix = SeaSurfaceTemperatureNameAdd('tos_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,tos,o,c,'sea_surface_temperature' "
            "/a/tos_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToThousandths(BaseTest):
    """ Test VarUnitsToThousandths """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToThousandths.
        """
        fix = VarUnitsToThousandths('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,so,o,c,'0.001' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


if __name__ == '__main__':
    unittest.main()
