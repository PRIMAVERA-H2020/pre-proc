"""
test_attribute_add.py

Unit tests for all FileFix concrete classes from attribute_add.py
"""
import subprocess
import unittest

import mock

from pre_proc.file_fix import (
    AirTemperatureNameAdd,
    ParentBranchTimeAdd,
    ChildBranchTimeAdd,
    BranchMethodAdd,
    BranchTimeDelete,
    DataSpecsVersionAdd,
    DataSpecsVersion27Add,
    DataSpecsVersion29Add,
    EcEarthInstitution,
    EcmwfInstitution,
    EcmwfReferences,
    EcmwfSourceHr,
    EcmwfSourceMr,
    EcmwfSourceLr,
    ExternalVariablesAreacella,
    ExternalVariablesAreacello,
    ExternalVariablesAreacelloVolcello,
    ForcingIndexFromFilename,
    FrequencyDayAdd,
    FrequencyMonAdd,
    GeopotentialHeightNameAdd,
    GridLabelGnAdd,
    GridLabelGrAdd,
    GridNativeAdd,
    HadGemMMParentSourceId,
    HistoryClearOld,
    InitializationIndexFromFilename,
    PhysicsIndexFromFilename,
    RealizationIndexFromFilename,
    CellMeasuresAreacellaAdd,
    CellMeasuresAreacelloAdd,
    CellMeasuresAreacelloVolcelloAdd,
    CellMeasuresDelete,
    CellMethodsAreaTimeMeanAdd,
    CellMethodsAreaMeanTimeLandMeanAdd,
    CellMethodsTimeMaxAdd,
    CellMethodsTimeMeanAdd,
    CellMethodsTimePointAdd,
    CellMethodsSeaAreaTimeMeanAdd,
    CellMethodsAreaMeanTimePointAdd,
    CellMethodsAreaTimeMeanAddLand,
    CellMethodsAreaMeanLandTimeMeanAdd,
    CellMethodsAreaMeanTimePointAddLand,
    CellMethodsAreaMeanLandTimePointAdd,
    CellMethodsAreaMeanTimeMinimumAdd,
    CellMethodsAreaMeanTimeMaximumAdd,
    CellMethodsAreaMeanTimeMinDailyAdd,
    CellMethodsAreaMeanTimeMaxDailyAdd,
    CellMethodsAreaSumSeaTimeMeanAdd,
    Conventions,
    CreationDate201807,
    DcppcAmvNegExpt,
    DcppcAmvNegExptId,
    DcppcAmvPosExpt,
    DcppcAmvPosExptId,
    ProductAdd,
    AtmosphereCloudIceContentStandardNameAdd,
    HfbasinpmadvStandardNameAdd,
    HfbasinpmdiffStandardNameAdd,
    SeaWaterSalinityStandardNameAdd,
    LicenseAdd,
    MipEraToPrim,
    MpiInstitution,
    MsftmzmpaStandardNameAdd,
    NominalResolution100km,
    NominalResolution50km,
    NominalResolution25km,
    NominalResolution10km,
    RealmAtmos,
    RealmOcean,
    RealmSeaIce,
    SeaSurfaceTemperatureNameAdd,
    ShallowConvectivePrecipitationFluxStandardNameAdd,
    SidmassdynStandardNameAdd,
    SidmassthStandardNameAdd,
    SiflcondbotStandardNameAdd,
    SiflfwbotStandardNameAdd,
    SiflsensupbotStandardNameAdd,
    SihcStandardNameAdd,
    SisaltmassStandardNameAdd,
    SistrxubotStandardNameAdd,
    SistryubotStandardNameAdd,
    SitempbotStandardNameAdd,
    SitimefracStandardNameAdd,
    SpecificHumidityStandardNameAdd,
    SurfaceTemperatureNameAdd,
    TrackingIdNew,
    UaStdNameAdd,
    VariantLabelFromFilename,
    VarUnitsTo1,
    VarUnitsToDegC,
    VarUnitsToKelvin,
    VarUnitsToMetre,
    VarUnitsToMetrePerSecond,
    VarUnitsToPascalPerSecond,
    VarUnitsToPercent,
    VarUnitsToThousandths,
    VaStdNameAdd,
    VerticesLatStdNameDelete,
    VerticesLonStdNameDelete,
    WapStandardNameAdd,
    WtemStandardNameAdd,
    WindSpeedStandardNameAdd,
    ZFurtherInfoUrl,
    ZZZThetapv2StandardNameAdd
)


class BaseTest(unittest.TestCase):
    """ Base class to setup a typical environment used by other tests """
    def setUp(self):
        """ Set up code run before every test """
        # mock any external calls
        patch = mock.patch('pre_proc.common.subprocess.check_output')
        self.mock_subprocess = patch.start()
        self.addCleanup(patch.stop)


class TestAirTemperatureNameAdd(BaseTest):
    """ Test AirTemperatureNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        AirTemperatureNameAdd
        """
        fix = AirTemperatureNameAdd('ta_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,ta,o,c,'air_temperature' "
            "/a/ta_components.nc",
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


class TestBranchTimeDelete(BaseTest):
    """ Test BranchTimeDelete """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ChildBranchTimeAdd
        """
        fix = BranchTimeDelete('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a branch_time,global,d,c,0 "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDataSpecsVersionAdd(BaseTest):
    """ Test DataSpecsVersionAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DataSpecsVersionAdd
        """
        fix = DataSpecsVersionAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a data_specs_version,global,o,c,'01.00.23' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDataSpecsVersion27Add(BaseTest):
    """ Test DataSpecsVersion27Add """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DataSpecsVersion27Add
        """
        fix = DataSpecsVersion27Add('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a data_specs_version,global,o,c,'01.00.27' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDataSpecsVersion29Add(BaseTest):
    """ Test DataSpecsVersion29Add """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DataSpecsVersion29Add
        """
        fix = DataSpecsVersion29Add('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a data_specs_version,global,o,c,'01.00.29' "
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


class TestCellMeasuresDelete(BaseTest):
    """ Test CellMeasuresDelete """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMeasuresDelete
        """
        fix = CellMeasuresDelete('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_measures,so,d,c,0 "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsTimeMaxAdd(BaseTest):
    """ Test CellMethodsTimeMaxAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsTimeMaxAdd
        """
        fix = CellMethodsTimeMaxAdd('sfcWindmax_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,sfcWindmax,o,c,'time: maximum' "
            "/a/sfcWindmax_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsTimeMeanAdd(BaseTest):
    """ Test CellMethodsTimeMeanAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsTimeMeanAdd
        """
        fix = CellMethodsTimeMeanAdd('tas_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,tas,o,c,'time: mean' "
            "/a/tas_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsTimePointAdd(BaseTest):
    """ Test CellMethodsTimePointAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsTimePointAdd
        """
        fix = CellMethodsTimePointAdd('ua_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,ua,o,c,'time: point' "
            "/a/ua_components.nc",
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


class TestCellMethodsAreaMeanTimeLandMeanAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimeLandMeanAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimeLandMeanAdd
        """
        fix = CellMethodsAreaMeanTimeLandMeanAdd('mrro_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,mrro,o,c,"
            "'area: mean where land time: mean' "
            "/a/mrro_components.nc",
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


class TestCellMethodsAreaTimeMeanAddLand(BaseTest):
    """ Test CellMethodsAreaTimeMeanAddLand """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaTimeMeanAddLand
        """
        fix = CellMethodsAreaTimeMeanAddLand('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,so,o,c,"
            "'area: time: mean (comment: over land and sea ice)' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaMeanTimePointAddLand(BaseTest):
    """ Test CellMethodsAreaMeanTimePointAddLand """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimePointAddLand
        """
        fix = CellMethodsAreaMeanTimePointAddLand('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,so,o,c,"
            "'area: mean (comment: over land and sea ice) time: point' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


# CellMethodsAreaMeanLandTimeMeanAdd
class TestCellMethodsAreaMeanLandTimeMeanAdd(BaseTest):
    """ Test CellMethodsAreaMeanLandTimeMeanAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanLandTimeMeanAdd
        """
        fix = CellMethodsAreaMeanLandTimeMeanAdd('mrso_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,mrso,o,c,"
            "'time: mean area: mean where land' "
            "/a/mrso_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaMeanLandTimePointAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimePointAddLand """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanLandTimePointAdd
        """
        fix = CellMethodsAreaMeanLandTimePointAdd('so_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,so,o,c,"
            "'area: mean where land time: point' "
            "/a/so_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaMeanTimeMinimumAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimeMinimumAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimeMinimumAdd
        """
        fix = CellMethodsAreaMeanTimeMinimumAdd('tasmin_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,tasmin,o,c,"
            "'area: mean time: minimum within days time: mean over days' "
            "/a/tasmin_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaMeanTimeMaximumAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimeMaximumAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimeMaximumAdd
        """
        fix = CellMethodsAreaMeanTimeMaximumAdd('tasmax_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,tasmax,o,c,"
            "'area: mean time: maximum within days time: mean over days' "
            "/a/tasmax_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaMeanTimeMinDailyAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimeMinDailyAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimeMinDailyAdd
        """
        fix = CellMethodsAreaMeanTimeMinDailyAdd('tasmin_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,tasmin,o,c,"
            "'area: mean time: minimum' "
            "/a/tasmin_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaMeanTimeMaxDailyAdd(BaseTest):
    """ Test CellMethodsAreaMeanTimeMaxDailyAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaMeanTimeMaxDailyAdd
        """
        fix = CellMethodsAreaMeanTimeMaxDailyAdd('sfcWindmax_components.nc',
                                                 '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,sfcWindmax,o,c,"
            "'area: mean time: maximum' "
            "/a/sfcWindmax_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCellMethodsAreaSumSeaTimeMeanAdd(BaseTest):
    """ Test CellMethodsAreaSumSeaTimeMeanAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CellMethodsAreaSumSeaTimeMeanAdd
        """
        fix = CellMethodsAreaSumSeaTimeMeanAdd('masso_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a cell_methods,masso,o,c,"
            "'area: sum where sea time: mean' "
            "/a/masso_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestConventions(BaseTest):
    """ Test Conventions """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        Conventions
        """
        fix = Conventions('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a Conventions,global,o,c,"
            "'CF-1.7 CMIP-6.2' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestCreationDate201807(BaseTest):
    """ Test CreationDate201807 """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        CreationDate201807
        """
        fix = CreationDate201807('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a creation_date,global,o,c,"
            "'2018-07-01T00:00:00Z' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDcppcAmvNegExpt(BaseTest):
    """ Test DcppcAmvNegExpt """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DcppcAmvNegExpt
        """
        fix = DcppcAmvNegExpt('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a experiment,global,o,c,"
            "'Idealized climate impact of negative 2xAMV anomaly pattern' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDcppcAmvNegExptId(BaseTest):
    """ Test DcppcAmvNegExptId """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DcppcAmvNegExptId
        """
        fix = DcppcAmvNegExptId('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a experiment_id,global,o,c,"
            "'dcppc-amv-neg' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDcppcAmvPosExpt(BaseTest):
    """ Test DcppcAmvPosExpt """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DcppcAmvPosExpt
        """
        fix = DcppcAmvPosExpt('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a experiment,global,o,c,"
            "'Idealized climate impact of positive 2xAMV anomaly pattern' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestDcppcAmvPosExptId(BaseTest):
    """ Test DcppcAmvPosExptId """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        DcppcAmvPosExptId
        """
        fix = DcppcAmvPosExptId('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a experiment_id,global,o,c,"
            "'dcppc-amv-pos' "
            "/a/var_components.nc",
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


class TestExternalVariablesAreacella(BaseTest):
    """ Test ExternalVariablesAreacella """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfSourceLr
        """
        fix = ExternalVariablesAreacella('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a external_variables,global,o,c,'areacella' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestExternalVariablesAreacello(BaseTest):
    """ Test ExternalVariablesAreacello """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfSourceLr
        """
        fix = ExternalVariablesAreacello('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a external_variables,global,o,c,'areacello' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestExternalVariablesAreacelloVolcello(BaseTest):
    """ Test ExternalVariablesAreacelloVolcello """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        EcmwfSourceLr
        """
        fix = ExternalVariablesAreacelloVolcello('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a external_variables,global,o,c,'areacello volcello' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestForcingIndexFromFilename(BaseTest):
    """ Test ForcingIndexFromFilename """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ForcingIndexFromFilename
        """
        fix = ForcingIndexFromFilename(
            'var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc',
            '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a forcing_index,global,o,s,10 "
            "/a/var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestFrequencyDayAdd(BaseTest):
    """ Test FrequencyDayAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        FrequencyDayAdd
        """
        fix = FrequencyDayAdd('var_cmpts.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a frequency,global,o,c,'day' /a/var_cmpts.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestFrequencyMonAdd(BaseTest):
    """ Test FrequencyMonAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        FrequencyMonAdd
        """
        fix = FrequencyMonAdd('var_cmpts.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a frequency,global,o,c,'mon' /a/var_cmpts.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestGeopotentialHeightNameAdd(BaseTest):
    """ Test GeopotentialHeightNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        GeopotentialHeightNameAdd
        """
        fix = GeopotentialHeightNameAdd('zg_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,zg,o,c,'geopotential_height' "
            "/a/zg_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestGridLabelGnAdd(BaseTest):
    """ Test GridLabelGnAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        GridLabelGnAdd
        """
        fix = GridLabelGnAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a grid_label,global,o,c,'gn' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestGridLabelGrAdd(BaseTest):
    """ Test GridLabelGrAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        GridLabelGrAdd
        """
        fix = GridLabelGrAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a grid_label,global,o,c,'gr' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestGridNativeAdd(BaseTest):
    """ Test GridNativeAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        GridNativeAdd
        """
        fix = GridNativeAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a grid,global,o,c,'native atmosphere and ocean grids' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestHadGemMMParentSourceId(BaseTest):
    """ Test HadGemMMParentSourceId """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        HadGemMMParentSourceId
        """
        fix = HadGemMMParentSourceId('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a parent_source_id,global,o,c,'HadGEM3-GC31-MM' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestHistoryClearOld(BaseTest):
    """ Test HistoryClearOld """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        HistoryClearOld
        """
        fix = HistoryClearOld('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a history,global,o,c,'' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestInitializationIndexFromFilename(BaseTest):
    """ Test InitializationIndexFromFilename """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        InitializationIndexFromFilename
        """
        fix = InitializationIndexFromFilename(
            'var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc',
            '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a initialization_index,global,o,s,2 "
            "/a/var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestPhysicsIndexFromFilename(BaseTest):
    """ Test PhysicsIndexFromFilename """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        PhysicsIndexFromFilename
        """
        fix = PhysicsIndexFromFilename(
            'var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc',
            '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a physics_index,global,o,s,3 "
            "/a/var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestRealizationIndexFromFilename(BaseTest):
    """ Test RealizationIndexFromFilename """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RealizationIndexFromFilename
        """
        fix = RealizationIndexFromFilename(
            'var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc',
            '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a realization_index,global,o,s,1 "
            "/a/var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestProductAdd(BaseTest):
    """ Test ProductAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for ProductAdd
        """
        fix = ProductAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a product,global,o,c,'model-output' /a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestAtmosphereCloudIceContentStandardNameAdd(BaseTest):
    """ Test AtmosphereCloudIceContentStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        AtmosphereCloudIceContentStandardNameAdd
        """
        fix = AtmosphereCloudIceContentStandardNameAdd('clivi_components.nc',
                                                       '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,clivi,o,c,"
            "'atmosphere_cloud_ice_content' "
            "/a/clivi_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestHfbasinpmadvStandardNameAdd(BaseTest):
    """ Test HfbasinpmadvStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        HfbasinpmadvStandardNameAdd
        """
        fix = HfbasinpmadvStandardNameAdd('hfbasinpmadv_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,hfbasinpmadv,o,c,"
            "'northward_ocean_heat_transport_due_to_parameterized_mesoscale_"
            "eddy_advection' "
            "/a/hfbasinpmadv_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestHfbasinpmdiffStandardNameAdd(BaseTest):
    """ Test HfbasinpmdiffStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        HfbasinpmdiffStandardNameAdd
        """
        fix = HfbasinpmdiffStandardNameAdd('hfbasinpmdiff_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,hfbasinpmdiff,o,c,"
            "'northward_ocean_heat_transport_due_to_parameterized_mesoscale_"
            "eddy_diffusion' "
            "/a/hfbasinpmdiff_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestLicenseAdd(BaseTest):
    """ Test LicenseAdd """
    @mock.patch('pre_proc.file_fix.attribute_add.Dataset')
    def test_subprocess_called_correctly(self, mock_dataset):
        """
        Test that an external call's been made correctly for
        LicenseAdd
        """
        class MockedDataset:
            institution_id = 'my-institution'
        mock_dataset.return_value.__enter__.return_value = MockedDataset

        fix = LicenseAdd('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a license,global,o,c,"
            "'CMIP6 model data produced by my-institution is licensed under a "
            "Creative Commons Attribution-ShareAlike 4.0 International License "
            "(https://creativecommons.org/licenses/). Consult https://pcmdi."
            "llnl.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 "
            "output, including citation requirements and proper "
            "acknowledgment. Further information about this data, including "
            "some limitations, can be found via the further_info_url (recorded "
            "as a global attribute in this file). The data producers and data "
            "providers make no warranty, either express or implied, including, "
            "but not limited to, warranties of merchantability and fitness for "
            "a particular purpose. All liabilities arising from the supply of "
            "the information (including any liability arising in negligence) "
            "are excluded to the fullest extent permitted by law.' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestMipEraToPrim(BaseTest):
    """ Test MipEraToPrim """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        MipEraToPrim
        """
        fix = MipEraToPrim('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a mip_era,global,o,c,'PRIMAVERA' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestMpiInstitution(BaseTest):
    """ Test MpiInstitution """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        MpiInstitution
        """
        fix = MpiInstitution('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a institution,global,o,c,"
            "'Max Planck Institute for Meteorology, Hamburg 20146, Germany' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestMsftmzmpaStandardNameAdd(BaseTest):
    """ Test MsftmzmpaStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        MsftmzmpaStandardNameAdd
        """
        fix = MsftmzmpaStandardNameAdd('msftmzmpa_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,msftmzmpa,o,c,'ocean_meridional_"
            "overturning_mass_streamfunction_due_to_parameterized_mesoscale_"
            "eddy_advection' /a/msftmzmpa_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestNominalResolution100km(BaseTest):
    """ Test NominalResolution100km """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        NominalResolution100km
        """
        fix = NominalResolution100km('file.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a nominal_resolution,global,o,c,'100 km' /a/file.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestNominalResolution50km(BaseTest):
    """ Test NominalResolution50km """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        NominalResolution50km
        """
        fix = NominalResolution50km('file.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a nominal_resolution,global,o,c,'50 km' /a/file.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestNominalResolution25km(BaseTest):
    """ Test NominalResolution25km """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        NominalResolution25km
        """
        fix = NominalResolution25km('file.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a nominal_resolution,global,o,c,'25 km' /a/file.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestNominalResolution10km(BaseTest):
    """ Test NominalResolution10km """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        NominalResolution10km
        """
        fix = NominalResolution10km('file.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a nominal_resolution,global,o,c,'10 km' /a/file.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestRealmAtmos(BaseTest):
    """ Test RealmAtmos """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RealmAtmos
        """
        fix = RealmAtmos('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a realm,global,o,c,'atmos' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestRealmOcean(BaseTest):
    """ Test RealmOcean """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RealmOcean
        """
        fix = RealmOcean('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a realm,global,o,c,'ocean' "
            "/a/var_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestRealmSeaIce(BaseTest):
    """ Test RealmSeaIce """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        RealmSeaIce
        """
        fix = RealmSeaIce('var_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a realm,global,o,c,'seaIce' "
            "/a/var_components.nc",
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


class TestSidmassdynStandardNameAdd(BaseTest):
    """ Test SidmassdynStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SidmassdynStandardNameAdd
        """
        fix = SidmassdynStandardNameAdd(
            'sidmassdyn_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sidmassdyn,o,c,"
            "'tendency_of_sea_ice_amount_due_to_sea_ice_dynamics' "
            "/a/sidmassdyn_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSidmassthStandardNameAdd(BaseTest):
    """ Test SidmassthStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SidmassthStandardNameAdd
        """
        fix = SidmassthStandardNameAdd(
            'sidmassth_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sidmassth,o,c,"
            "'tendency_of_sea_ice_amount_due_to_sea_ice_thermodynamics' "
            "/a/sidmassth_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSiflcondbotStandardNameAdd(BaseTest):
    """ Test SiflcondbotStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SiflcondbotStandardNameAdd
        """
        fix = SiflcondbotStandardNameAdd(
            'siflcondbot_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,siflcondbot,o,c,"
            "'sea_ice_basal_net_downward_sensible_heat_flux' "
            "/a/siflcondbot_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSiflfwbotStandardNameAdd(BaseTest):
    """ Test SiflfwbotStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SiflfwbotStandardNameAdd
        """
        fix = SiflfwbotStandardNameAdd(
            'siflfwbot_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,siflfwbot,o,c,"
            "'water_flux_into_sea_water_from_sea_ice' "
            "/a/siflfwbot_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSiflsensupbotStandardNameAdd(BaseTest):
    """ Test SiflsensupbotStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SiflsensupbotStandardNameAdd
        """
        fix = SiflsensupbotStandardNameAdd(
            'siflsensupbot_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,siflsensupbot,o,c,"
            "'upward_sea_ice_basal_heat_flux' "
            "/a/siflsensupbot_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSihcStandardNameAdd(BaseTest):
    """ Test SihcStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SihcStandardNameAdd
        """
        fix = SihcStandardNameAdd(
            'sihc_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sihc,o,c,"
            "'sea_ice_temperature_expressed_as_heat_content' "
            "/a/sihc_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSisaltmassStandardNameAdd(BaseTest):
    """ Test SisaltmassStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SisaltmassStandardNameAdd
        """
        fix = SisaltmassStandardNameAdd(
            'sisaltmass_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sisaltmass,o,c,"
            "'sea_ice_salt_content' "
            "/a/sisaltmass_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSistrxubotStandardNameAdd(BaseTest):
    """ Test SistrxubotStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SistrxubotStandardNameAdd
        """
        fix = SistrxubotStandardNameAdd(
            'sistrxubot_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sistrxubot,o,c,"
            "'upward_x_stress_at_sea_ice_base' "
            "/a/sistrxubot_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSistryubotStandardNameAdd(BaseTest):
    """ Test SistryubotStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SistryubotStandardNameAdd
        """
        fix = SistryubotStandardNameAdd(
            'sistryubot_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sistryubot,o,c,"
            "'upward_y_stress_at_sea_ice_base' "
            "/a/sistryubot_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSitempbotStandardNameAdd(BaseTest):
    """ Test SitempbotStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SitempbotStandardNameAdd
        """
        fix = SitempbotStandardNameAdd(
            'sitempbot_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sitempbot,o,c,"
            "'sea_ice_basal_temperature' "
            "/a/sitempbot_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSitimefracStandardNameAdd(BaseTest):
    """ Test SitimefracStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SitimefracStandardNameAdd
        """
        fix = SitimefracStandardNameAdd(
            'sitimefrac_components.nc', '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sitimefrac,o,c,"
            "'fraction_of_time_with_sea_ice_area_fraction_above_threshold' "
            "/a/sitimefrac_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSpecificHumidityStandardNameAdd(BaseTest):
    """ Test SpecificHumidityStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SpecificHumidityStandardNameAdd
        """
        fix = SpecificHumidityStandardNameAdd('hus_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,hus,o,c,'specific_humidity' "
            "/a/hus_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestSurfaceTemperatureNameAdd(BaseTest):
    """ Test SurfaceTemperatureNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        SurfaceTemperatureNameAdd
        """
        fix = SurfaceTemperatureNameAdd('ts_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,ts,o,c,'surface_temperature' "
            "/a/ts_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestTrackingIdNew(BaseTest):
    """ Test TrackingIdNew """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        ShallowConvectivePrecipitationFluxStandardNameAdd
        """
        fix = TrackingIdNew('prcsh_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once()
        self.assertRegex(self.mock_subprocess.call_args[0][0],
                         r"ncatted -h -a tracking_id,global,o,c,"
                         r"'hdl:21.14100/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}' "
                         r"/a/prcsh_components.nc")


class TestUaStdNameAdd(BaseTest):
    """ Test UaStdNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for UaStdNameAdd
        """
        fix = UaStdNameAdd('ua_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,ua,o,c,'eastward_wind' "
            "/a/ua_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVariantLabelFromFilename(BaseTest):
    """ Test VariantLabelFromFilename """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VariantLabelFromFilename.
        """
        fix = VariantLabelFromFilename(
            'var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc',
            '/a'
        )
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a variant_label,global,o,c,'r1i2p3f10' "
            "/a/var_Table_Model-id_Expt-id_r1i2p3f10_gn_195601-195612.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsTo1(BaseTest):
    """ Test VarUnitsTo1 """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsTo1.
        """
        fix = VarUnitsTo1('hus_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,hus,o,c,'1' "
            "/a/hus_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToDegC(BaseTest):
    """ Test VarUnitsToDegC """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToDegC.
        """
        fix = VarUnitsToDegC('tos_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,tos,o,c,'degC' "
            "/a/tos_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToKelvin(BaseTest):
    """ Test VarUnitsToKelvin """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToKelvin.
        """
        fix = VarUnitsToKelvin('ts_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,ts,o,c,'K' "
            "/a/ts_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToMetre(BaseTest):
    """ Test VarUnitsToMetre """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToMetre.
        """
        fix = VarUnitsToMetre('zg_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,zg,o,c,'m' "
            "/a/zg_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToMetrePerSecond(BaseTest):
    """ Test VarUnitsToMetrePerSecond """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToMetrePerSecond.
        """
        fix = VarUnitsToMetrePerSecond('ua_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,ua,o,c,'m s-1' "
            "/a/ua_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToPascalPerSecond(BaseTest):
    """ Test VarUnitsToPascalPerSecond """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToPascalPerSecond.
        """
        fix = VarUnitsToPascalPerSecond('wap_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,wap,o,c,'Pa s-1' "
            "/a/wap_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVarUnitsToPercent(BaseTest):
    """ Test VarUnitsToPercent """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VarUnitsToPercent.
        """
        fix = VarUnitsToPercent('clt_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a units,clt,o,c,'%' "
            "/a/clt_components.nc",
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


class TestVaStdNameAdd(BaseTest):
    """ Test VaStdNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for VaStdNameAdd
        """
        fix = VaStdNameAdd('va_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,va,o,c,'northward_wind' "
            "/a/va_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVerticesLatStdNameDelete(BaseTest):
    """ Test VerticesLatStdNameDelete """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VerticesLatStdNameDelete
        """
        fix = VerticesLatStdNameDelete('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,vertices_latitude,d,c,0 "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestVerticesLonStdNameDelete(BaseTest):
    """ Test VerticesLonStdNameDelete """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        VerticesLonStdNameDelete
        """
        fix = VerticesLonStdNameDelete('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,vertices_longitude,d,c,0 "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestWapStandardNameAdd(BaseTest):
    """ Test WapStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        WapStandardNameAdd
        """
        fix = WapStandardNameAdd('wap_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,wap,o,c,"
            "'lagrangian_tendency_of_air_pressure' "
            "/a/wap_components.nc",
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


class TestWindSpeedStandardNameAdd(BaseTest):
    """ Test WindSpeedStandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        WindSpeedStandardNameAdd
        """
        fix = WindSpeedStandardNameAdd('sfcWindmax_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,sfcWindmax,o,c,"
            "'wind_speed' "
            "/a/sfcWindmax_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestZFurtherInfoUrl(BaseTest):
    """ Test ZFurtherInfoUrl """
    @mock.patch('pre_proc.file_fix.attribute_add.Dataset')
    def test_subprocess_called_correctly(self, mock_dataset):
        """
        Test that an external call's been made correctly for
        ZFurtherInfoUrl
        """
        class MockedDataset:
            mip_era = 'mip_era'
            institution_id = 'institution_id'
            source_id = 'source_id'
            experiment_id = 'experiment_id'
            sub_experiment_id = 'none'
            variant_label = 'variant_label'
        mock_dataset.return_value.__enter__.return_value = MockedDataset

        fix = ZFurtherInfoUrl('1.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a further_info_url,global,o,c,"
            "'https://furtherinfo.es-doc.org/mip_era.institution_id.source_id."
            "experiment_id.none.variant_label' "
            "/a/1.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


class TestZZZThetapv2StandardNameAdd(BaseTest):
    """ Test ZZZThetapv2StandardNameAdd """
    def test_subprocess_called_correctly(self):
        """
        Test that an external call's been made correctly for
        WindSpeedStandardNameAdd
        """
        fix = ZZZThetapv2StandardNameAdd('thetapv2_components.nc', '/a')
        fix.apply_fix()
        self.mock_subprocess.assert_called_once_with(
            "ncatted -h -a standard_name,thetapv2,o,c,"
            "'theta_on_pv2_surface' "
            "/a/thetapv2_components.nc",
            stderr=subprocess.STDOUT,
            shell=True
        )


if __name__ == '__main__':
    unittest.main()
