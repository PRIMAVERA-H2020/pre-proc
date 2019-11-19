"""
attribute_add.py

Workers that fix the netCDF files that are based on the AttributeAdd
abstract base classes.
"""
import uuid

from .abstract import AttributeAdd, AttributeDelete


class ParentBranchTimeAdd(AttributeAdd):
    """
   Add a global attribute `branch_time_in_parent` with a value of zero.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_parent'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 0.0


class ChildBranchTimeAdd(AttributeAdd):
    """
    Add a global attribute `branch_time_in_child` with a value of zero.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_time_in_child'
        self.attribute_visibility = 'global'
        self.attribute_type = 'd'

    def _calculate_new_value(self):
        """
        The new value is zero.
        """
        self.new_value = 0.0


class BranchMethodAdd(AttributeAdd):
    """
    Add a global attribute `branch_method` with a value of 'no_parent'.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'branch_method'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'no parent'


class DataSpecsVersionAdd(AttributeAdd):
    """
    Add a global attribute `data_specs_version` with a value of '01.00.23'.

    This will probably already exist but the parent abstract class uses
    overwrite and so this should be fine.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'data_specs_version'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '01.00.23'


class CellMeasuresAreacellaAdd(AttributeAdd):
    """
    Add a variable attribute `cellmeasures` with a value of `area: areacella`
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: areacella'


class CellMeasuresAreacelloAdd(AttributeAdd):
    """
    Add a variable attribute `cellmeasures` with a value of `area: areacello`
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: areacello'


class CellMeasuresAreacelloVolcelloAdd(AttributeAdd):
    """
    Add a variable attribute `cellmeasures` with a value of
    `area: areacello volume: volcello`
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: areacello volume: volcello'


class CellMeasuresDelete(AttributeDelete):
    """
    Delete variable attribute `cellmeasures`.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_measures'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        We're deleting so there's nothing to do but make a dummy value for
        new_value.
        """
        self.new_value = 0


class CellMethodsAreaTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of `area: time: mean`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: time: mean'


class CellMethodsSeaAreaTimeMeanAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean where sea time: mean`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean where sea time: mean'


class CellMethodsAreaMeanTimePointAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: point`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean time: point'


class CellMethodsAreaMeanTimeMinimumAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: minimum within days time: mean over days`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('area: mean time: minimum within days time: '
                          'mean over days')


class CellMethodsAreaMeanTimeMaximumAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: maximum within days time: mean over days`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('area: mean time: maximum within days time: '
                          'mean over days')


class CellMethodsAreaMeanTimeMinDailyAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: minimum`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean time: minimum'


class CellMethodsAreaMeanTimeMaxDailyAdd(AttributeAdd):
    """
    Add a variable attribute `cellmethods` with a value of
    `area: mean time: maximum`. This is done
    in overwrite mode and so will work irrespective of whether there is an
    existing cellmethods attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'cell_methods'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'area: mean time: maximum'


class EcEarthInstitution(AttributeAdd):
    """
    Add a global attribute `institution` with a value for EC-Earth. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'institution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, '
                          'Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany;'
                          ' ICHEC, Ireland; ICTP, Italy; IDL, Portugal; IMAU, '
                          'The Netherlands; IPMA, Portugal; KIT, Karlsruhe, '
                          'Germany; KNMI, The Netherlands; Lund University, '
                          'Sweden; Met Eireann, Ireland; NLeSC, The '
                          'Netherlands; NTNU, Norway; Oxford University, '
                          'UK; surfSARA, The Netherlands; SMHI, Sweden; '
                          'Stockholm University, Sweden; Unite ASTR, Belgium; '
                          'University College Dublin, Ireland; University of '
                          'Bergen, Norway; University of Copenhagen, Denmark; '
                          'University of Helsinki, Finland; University of '
                          'Santiago de Compostela, Spain; Uppsala University, '
                          'Sweden; Utrecht University, The Netherlands; Vrije '
                          'Universiteit Amsterdam, the Netherlands; Wageningen '
                          'University, The Netherlands. Mailing address: '
                          'EC-Earth consortium, Rossby Center, Swedish '
                          'Meteorological and Hydrological Institute/SMHI, '
                          'SE-601 76 Norrkoping, Sweden')


class EcmwfInstitution(AttributeAdd):
    """
    Add a global attribute `institution` with a value for ECMWF. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'institution'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('European Centre for Medium-Range Weather '
                          'Forecasts, Reading RG2 9AX, UK')


class EcmwfReferences(AttributeAdd):
    """
    Add a global attribute `referencs` with a value for ECMWF. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'references'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('Roberts, C. D., Senan, R., Molteni, F., Boussetta, '
                          'S., Mayer, M., and Keeley, S. P. E.: Climate model '
                          'configurations of the ECMWF Integrated Forecasting '
                          'System (ECMWF-IFS cycle 43r1) for HighResMIP, '
                          'Geosci. Model Dev., 11, 3681-3712, '
                          'https://doi.org/10.5194/gmd-11-3681-2018, 2018.')


class EcmwfSourceHr(AttributeAdd):
    """
    Add a global attribute `source` with a value for ECMWF-IFS-HR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'ECMWF-IFS-HR (2017): \naerosol: none\natmos: IFS (IFS CY43R1, '
            'Tco399, cubic octahedral reduced Gaussian grid equivalent to '
            '1600 x 800 longitude/latitude; 91 levels; top level 0.01 hPa)'
            '\natmosChem: none\nland: HTESSEL (as implemented in IFS CY43R1)'
            '\nlandIce: none\nocean: NEMO3.4 (NEMO v3.4; ORCA025 tripolar grid;'
            ' 1442 x 1021 longitude/latitude; 75 levels; top grid cell 0-1 m)'
            '\nocnBgchem: none\nseaIce: LIM2 (LIM v2; ORCA025 tripolar grid; '
            '1442 x 1021 longitude/latitude)'
        )


class EcmwfSourceMr(AttributeAdd):
    """
    Add a global attribute `source` with a value for ECMWF-IFS-MR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'ECMWF-IFS-MR (2017): \naerosol: none\natmos: IFS (IFS CY43R1, '
            'Tco199, cubic octahedral reduced Gaussian grid equivalent to 800 '
            'x 400 longitude/latitude; 91 levels; top level 0.01 hPa)'
            '\natmosChem: none\nland: HTESSEL (as implemented in IFS CY43R1)'
            '\nlandIce: none\nocean: NEMO3.4 (NEMO v3.4; ORCA025 tripolar '
            'grid; 1442 x 1021 longitude/latitude; 75 levels; top grid cell '
            '0-1 m)\nocnBgchem: none\nseaIce: LIM2 (LIM v2; ORCA025 tripolar '
            'grid; 1442 x 1021 longitude/latitude)'
        )


class EcmwfSourceLr(AttributeAdd):
    """
    Add a global attribute `source` with a value for ECMWF-IFS-LR. This
    is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'source'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = (
            'ECMWF-IFS-LR (2017): \naerosol: none\natmos: IFS (IFS CY43R1, '
            'Tco199, cubic octahedral reduced Gaussian grid equivalent to 800 '
            'x 400 longitude/latitude; 91 levels; top level 0.01 hPa)'
            '\natmosChem: none\nland: HTESSEL (as implemented in IFS CY43R1)'
            '\nlandIce: none\nocean: NEMO3.4 (NEMO v3.4; ORCA1 tripolar grid; '
            '362 x 292 longitude/latitude; 75 levels; top grid cell 0-1 m)'
            '\nocnBgchem: none\nseaIce: LIM2 (LIM v2; ORCA1 tripolar grid; '
            '362 x 292 longitude/latitude)'
        )


class ExternalVariablesAreacella(AttributeAdd):
    """
    Add a global attribute `external_variables` with a value of `areacella`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'external_variables'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'areacella'


class ExternalVariablesAreacello(AttributeAdd):
    """
    Add a global attribute `external_variables` with a value of `areacello`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'external_variables'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'areacello'


class ExternalVariablesAreacelloVolcello(AttributeAdd):
    """
    Add a global attribute `external_variables` with a value of
    `areacello volcello`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'external_variables'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'areacello volcello'


class HadGemMMParentSourceId(AttributeAdd):
    """
    Add a global attribute `parent_source_id` with a value for HadGEM3-GC31-MM.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'parent_source_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'HadGEM3-GC31-MM'


class ProductAdd(AttributeAdd):
    """
    Add a global attribute `product` with a value of `model-output`. This is
    done in overwrite mode and so will work irrespective of whether there is
    an existing attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'product'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'model-output'


class AtmosphereCloudIceContentStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `atmosphere_cloud_ice_content`. This is done in overwrite mode and so will
    work irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'atmosphere_cloud_ice_content'


class HfbasinpmadvStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `northward_ocean_heat_transport_due_to_parameterized_mesoscale_eddy_advection`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('northward_ocean_heat_transport_due_to_'
                          'parameterized_mesoscale_eddy_advection')


class HfbasinpmdiffStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `northward_ocean_heat_transport_due_to_parameterized_mesoscale_eddy_diffusion`.
    This is done in overwrite mode and so will work irrespective of whether
    there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('northward_ocean_heat_transport_due_to_'
                          'parameterized_mesoscale_eddy_diffusion')


class MsftmzmpaStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `ocean_meridional_overturning_mass_streamfunction_due_to_parameterized_
    mesoscale_eddy_advection`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = ('ocean_meridional_overturning_mass_streamfunction_'
                          'due_to_parameterized_mesoscale_eddy_advection')


class SeaWaterSalinityStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_water_salinity`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_water_salinity'


class SeaSurfaceTemperatureNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_surface_temperature`. This is done in overwrite mode and so will work
    irrespective of whether there is an existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_surface_temperature'


class ShallowConvectivePrecipitationFluxStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `shallow_convective_precipitation_flux`. This is done in overwrite mode
    and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'shallow_convective_precipitation_flux'


class SiflcondbotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_ice_basal_net_downward_sensible_heat_flux`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_ice_basal_net_downward_sensible_heat_flux'


class SiflfwbotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `water_flux_into_sea_water_from_sea_ice`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'water_flux_into_sea_water_from_sea_ice'


class SisaltmassStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `sea_ice_salt_content`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'sea_ice_salt_content'


class SistrxubotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `upward_x_stress_at_sea_ice_base`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_x_stress_at_sea_ice_base'


class SistryubotStandardNameAdd(AttributeAdd):
    """
    Add a variable attribute `standard_name` with a value of
    `upward_y_stress_at_sea_ice_base`. This is done in overwrite
    mode and so will work irrespective of whether there is an existing
    standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_y_stress_at_sea_ice_base'


class TrackingIdNew(AttributeAdd):
    """
    Replace the tracking_id attribute with a new value. This may be useful
    when resubmitting files that have been retracted.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'tracking_id'
        self.attribute_visibility = 'global'
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = f'hdl:21.14100/{uuid.uuid4()}'


class VarUnitsToPercent(AttributeAdd):
    """
    Replace the variable's attribute `units` to `%`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '%'


class VarUnitsToThousandths(AttributeAdd):
    """
    Replace the variable's attribute `units` to `0.001`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing units attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'units'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = '0.001'


class WtemStandardNameAdd(AttributeAdd):
    """
    Replace the variable's `standard_name` with
    `upward_transformed_eulerian_mean_air_velocity`. This is done in
    overwrite mode and so will work irrespective of whether there is an
    existing standard_name attribute.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        super().__init__(filename, directory)
        self.attribute_name = 'standard_name'
        self.attribute_visibility = self.variable_name
        self.attribute_type = 'c'

    def _calculate_new_value(self):
        """
        Set the new value.
        """
        self.new_value = 'upward_transformed_eulerian_mean_air_velocity'
