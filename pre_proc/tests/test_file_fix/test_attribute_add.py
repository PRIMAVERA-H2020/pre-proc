"""
test_attribute_add.py

Unit tests for all FileFix concrete classes from attribute_add.py
"""
import subprocess
import unittest

import mock

from pre_proc.file_fix import (ParentBranchTimeAdd,
                               ChildBranchTimeAdd,
                               BranchMethodAdd,
                               DataSpecsVersionAdd,
                               DataSpecsVersionAddTwentySeven,
                               EcmwfInstitution,
                               CellMeasuresAreacellaAdd,
                               CellMeasuresAreacelloAdd,
                               CellMeasuresAreacelloVolcelloAdd,
                               CellMethodsAreaTimeMeanAdd,
                               CellMethodsSeaAreaTimeMeanAdd,
                               SeaWaterSalinityStandardNameAdd,
                               SeaSurfaceTemperatureNameAdd,
                               VarUnitsToThousandths,
                               WtemStandardNameAdd)


class BaseTest(unittest.TestCase):
    """ Base class to setup a typical environment used by other tests """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)


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


class TestDataSpecsVersionAddTwentySeven(BaseTest):
    """ Test DataSpecsVersionTwentySeven """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeAdd
        """
        fix = DataSpecsVersionAddTwentySeven('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a data_specs_version,global,o,c,'01.00.27' "
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


class TestEcmwfInstitution(BaseTest):
    """ Test EcmwfInstitution """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeAdd
        """
        fix = EcmwfInstitution('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a institution,global,o,c,'European Centre for Medium-"
            "Range Weather Forecasts, Reading RG2 9AX, UK' "
            "/a/1.nc",
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


class TestWtemStandardNameAdd(BaseTest):
    """ Test WtemStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        WtemStandardNameAdd
        """
        fix = WtemStandardNameAdd('wtem_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,wtem,o,c,"
            "'upward_transformed_eulerian_mean_air_velocity' "
            "/a/wtem_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


if __name__ == '__main__':
    unittest.main()
