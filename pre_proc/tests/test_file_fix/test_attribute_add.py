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
                               EcEarthInstitution,
                               EcmwfInstitution,
                               EcmwfReferences,
                               EcmwfSourceHr,
                               EcmwfSourceMr,
                               EcmwfSourceLr,
                               CellMeasuresAreacellaAdd,
                               CellMeasuresAreacelloAdd,
                               CellMeasuresAreacelloVolcelloAdd,
                               CellMethodsAreaTimeMeanAdd,
                               CellMethodsSeaAreaTimeMeanAdd,
                               CellMethodsAreaMeanTimePointAdd,
                               SeaWaterSalinityStandardNameAdd,
                               SeaSurfaceTemperatureNameAdd,
                               ShallowConvectivePrecipitationFluxStandardNameAdd,
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


class TestCellMethodsAreaMeanTimePointAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimePointAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimePointAdd
        """
        fix = CellMethodsAreaMeanTimePointAdd('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,so,o,c,"
            "'area: mean time: point' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestEcEartInstitution(BaseTest):
    """ Test EcEarthInstitution """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcEarthInstitution
        """
        fix = EcEarthInstitution('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a institution,global,o,c,'AEMET, Spain; BSC, Spain; "
            "CNR-ISAC, Italy; DMI, Denmark; ENEA, Italy; FMI, Finland; Geomar, "
            "Germany; ICHEC, Ireland; ICTP, Italy; IDL, Portugal; IMAU, The "
            "Netherlands; IPMA, Portugal; KIT, Karlsruhe, Germany; KNMI, The "
            "Netherlands; Lund University, Sweden; Met Eireann, Ireland; "
            "NLeSC, The Netherlands; NTNU, Norway; Oxford University, UK; "
            "surfSARA, The Netherlands; SMHI, Sweden; Stockholm University, "
            "Sweden; Unite ASTR, Belgium; University College Dublin, Ireland; "
            "University of Bergen, Norway; University of Copenhagen, Denmark; "
            "University of Helsinki, Finland; University of Santiago de "
            "Compostela, Spain; Uppsala University, Sweden; Utrecht "
            "University, The Netherlands; Vrije Universiteit Amsterdam, the "
            "Netherlands; Wageningen University, The Netherlands. Mailing "
            "address: EC-Earth consortium, Rossby Center, Swedish "
            "Meteorological and Hydrological Institute/SMHI, SE-601 76 "
            "Norrkoping, Sweden' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestEcmwfInstitution(BaseTest):
    """ Test EcmwfInstitution """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfInstitution
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


class TestEcmwfReferences(BaseTest):
    """ Test EcmwfReferences """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfReferences
        """
        fix = EcmwfReferences('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a references,global,o,c,'Roberts, C. D., Senan, R., "
            "Molteni, F., Boussetta, S., Mayer, M., and Keeley, S. P. E.: "
            "Climate model configurations of the ECMWF Integrated Forecasting "
            "System (ECMWF-IFS cycle 43r1) for HighResMIP, Geosci. Model Dev., "
            "11, 3681-3712, https://doi.org/10.5194/gmd-11-3681-2018, 2018.' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestEcmwfSourceHr(BaseTest):
    """ Test EcmwfSourceHr """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfSourceHr
        """
        fix = EcmwfSourceHr('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a source,global,o,c,'ECMWF-IFS-HR (2017): "
            "\naerosol: none\natmos: IFS (IFS CY43R1, Tco399, cubic "
            "octahedral reduced Gaussian grid equivalent to 1600 x 800 "
            "longitude/latitude; 91 levels; top level 0.01 hPa)\natmosChem: "
            "none\nland: HTESSEL (as implemented in IFS CY43R1)\nlandIce: none"
            "\nocean: NEMO3.4 (NEMO v3.4; ORCA025 tripolar grid; 1442 x 1021 "
            "longitude/latitude; 75 levels; top grid cell 0-1 m)\nocnBgchem: "
            "none\nseaIce: LIM2 (LIM v2; ORCA025 tripolar grid; 1442 x 1021 "
            "longitude/latitude)' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestEcmwfSourceMr(BaseTest):
    """ Test EcmwfSourceMr """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfSourceMr
        """
        fix = EcmwfSourceMr('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a source,global,o,c,'ECMWF-IFS-MR (2017): "
            "\naerosol: none\natmos: IFS (IFS CY43R1, Tco199, cubic octahedral "
            "reduced Gaussian grid equivalent to 800 x 400 longitude/latitude; "
            "91 levels; top level 0.01 hPa)\natmosChem: none\nland: HTESSEL "
            "(as implemented in IFS CY43R1)\nlandIce: none\nocean: NEMO3.4 "
            "(NEMO v3.4; ORCA025 tripolar grid; 1442 x 1021 longitude/latitude;"
            " 75 levels; top grid cell 0-1 m)\nocnBgchem: none\nseaIce: LIM2 "
            "(LIM v2; ORCA025 tripolar grid; 1442 x 1021 longitude/latitude)' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestEcmwfSourceLr(BaseTest):
    """ Test EcmwfSourceLr """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfSourceLr
        """
        fix = EcmwfSourceLr('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a source,global,o,c,'ECMWF-IFS-LR (2017): "
            "\naerosol: none\natmos: IFS (IFS CY43R1, Tco199, cubic "
            "octahedral reduced Gaussian grid equivalent to 800 x 400 "
            "longitude/latitude; 91 levels; top level 0.01 hPa)\natmosChem: "
            "none\nland: HTESSEL (as implemented in IFS CY43R1)\nlandIce: "
            "none\nocean: NEMO3.4 (NEMO v3.4; ORCA1 tripolar grid; 362 x 292 "
            "longitude/latitude; 75 levels; top grid cell 0-1 m)\nocnBgchem: "
            "none\nseaIce: LIM2 (LIM v2; ORCA1 tripolar grid; 362 x 292 "
            "longitude/latitude)' "
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


class TestShallowConvectivePrecipitationFluxStandardNameAdd(BaseTest):
    """ Test ShallowConvectivePrecipitationFluxStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ShallowConvectivePrecipitationFluxStandardNameAdd
        """
        fix = ShallowConvectivePrecipitationFluxStandardNameAdd(
            'prcsh_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,prcsh,o,c,"
            "'shallow_convective_precipitation_flux' "
            "/a/prcsh_components.nc",
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
