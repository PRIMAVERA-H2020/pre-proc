"""
abstract.py

The abstract base file fixes.
"""
from abc import ABCMeta, abstractmethod
import os
import shutil
import traceback

from netCDF4 import Dataset

from pre_proc.common import run_command
from pre_proc.exceptions import (AttributeNotFoundError,
                                 InstanceVariableNotDefinedError,
                                 Ncap2Error, NcattedError, NcksError)


class FileFix(object, metaclass=ABCMeta):
    """
    The abstract base class that all fixes are made from
    """

    def __init__(self, filename, directory):
        """
        Initialise the class

        :param str filename: The basename of the file to process.
        :param str directory: The directory that the file is currently in.
        """
        self.filename = filename
        self.directory = directory
        self.variable_name = self.filename.split('_')[0]

    @abstractmethod
    def apply_fix(self):
        pass


class AttributeEdit(FileFix, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        # The name of the attribute to fix
        self.attribute_name = None
        # The var_nm to pass to ncatted, e.g. global for a global
        # attribute
        self.attribute_visibility = None
        # The var_nm to pass to ncatted, e.g. global for a global
        # attribute
        self.attribute_type = None

        # The new value of the required attributes
        self.new_value = None

    @abstractmethod
    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        pass

    @abstractmethod
    def _calculate_new_value(self):
        """
        From the existing value of the attribute, calculate the new value
        """
        pass

    def _run_ncatted(self, nco_mode):
        """
        Run the command

        :param str nco_mode: The mode to run nco in.
        """
        for attr_name in ['attribute_name', 'attribute_visibility',
                          'new_value']:
            attr_value = getattr(self, attr_name, None)
            if attr_value is None:
                raise InstanceVariableNotDefinedError(type(self).__name__,
                                                      attr_name)

        # Aiming for:
        # ncatted -h -a branch_time_in_parent,global,o,d,10800.0

        quote_mark = "'" if isinstance(self.new_value, str) else ""

        cmd = 'ncatted -h -a {},{},{},{},{}{}{} {}'.format(
            self.attribute_name,
            self.attribute_visibility,
            nco_mode,
            self.attribute_type,
            quote_mark,
            self.new_value,
            quote_mark,
            os.path.join(self.directory, self.filename)
        )
        try:
            run_command(cmd)
        except Exception:
            raise NcattedError(type(self).__name__, self.filename, cmd,
                               traceback.format_exc())


class DataFix(FileFix, metaclass=ABCMeta):
    """
    An abstract base class for fixes that edit the data in a netCDF file.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)


class NcoDataFix(DataFix, metaclass=ABCMeta):
    """
    An abstract base class for fixes that edit the data in a netCDF file
    using the NCO tools. The specified command is run and the input and output
    names are appended by this class.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        self.command = None

    def _run_nco_command(self, command_error):
        """
        Run the nco command
        """
        output_file = os.path.join(self.directory, self.filename)
        temp_file = output_file + '.temp'
        # Remove any temporary file left over from a previous failed
        # run as it could prevent some nco commands from running.
        if os.path.exists(temp_file):
            os.remove(temp_file)

        cmd = f'{self.command} {output_file} {temp_file}'
        try:
            run_command(cmd)
        except Exception:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise command_error(type(self).__name__, self.filename, cmd,
                                traceback.format_exc())

        os.remove(output_file)
        os.rename(temp_file, output_file)


class NcksAppendDataFix(DataFix, metaclass=ABCMeta):
    """
    An abstract base class for fixes that edit the data in a netCDF file
    using ncks to append a reference file into the specified file. The file
    to append should be specified in the command and the specified file's name
    will be added to this by the class when the command is run.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        self.command = None

    def _run_ncks_command(self):
        """
        Run the nco command.
        """
        output_file = os.path.join(self.directory, self.filename)
        temp_file = output_file + '.temp'
        # Remove any temporary file left over from a previous failed
        # run as it could prevent some nco commands from running.
        if os.path.exists(temp_file):
            os.remove(temp_file)

        shutil.copyfile(output_file, temp_file)

        cmd = f'{self.command} {temp_file}'
        try:
            run_command(cmd)
        except Exception:
            os.remove(temp_file)
            raise NcksError(type(self).__name__, self.filename, cmd,
                            traceback.format_exc())
        else:
            os.remove(output_file)
            os.rename(temp_file, output_file)


class AttributeUpdate(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    fix a metadata attribute.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

        # The current value of the required attributes
        self.existing_value = None

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._get_existing_value()
        self._calculate_new_value()
        self._run_ncatted('o')

    def _get_existing_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.existing_value = getattr(rootgrp, self.attribute_name, None)

        if self.existing_value is None:
            raise AttributeNotFoundError(self.filename, self.attribute_name)


class CopyAttribute(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """

    @abstractmethod
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

        # The name of the attribute to copy
        self.source_attribute = None

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted('o')

    @abstractmethod
    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        raise NotImplementedError()


class CopyGlobalAttribute(CopyAttribute, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """

    @abstractmethod
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            self.new_value = getattr(rootgrp, self.source_attribute, None)

        if self.new_value is None:
            raise AttributeNotFoundError(self.filename, self.source_attribute)


class CopyVariableAttribute(CopyAttribute, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    copy a metadata value from one attribute to another.
    """

    @abstractmethod
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def _calculate_new_value(self):
        """
        Get the value of the existing attribute from the current file
        """
        def raise_error():
            """ Raise AttributeNotFoundError """
            raise AttributeNotFoundError(
                self.filename,
                '{}.{}'.format(self.variable_name, self.source_attribute)
            )
        filepath = os.path.join(self.directory, self.filename)
        with Dataset(filepath) as rootgrp:
            netcdf_vars = getattr(rootgrp, 'variables', None)
            if netcdf_vars is None:
                raise_error()
            if self.variable_name not in netcdf_vars:
                raise_error()
            self.new_value = getattr(netcdf_vars[self.variable_name],
                                     self.source_attribute, None)
        if self.new_value is None:
            raise_error()


class AttributeAdd(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    add a new metadata attribute.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted('o')


class AttributeDelete(AttributeEdit, metaclass=ABCMeta):
    """
    An abstract base class for fixes that require the use of `ncatted` to
    remove a metadata attribute.

    _calculate_new_value() doesn't do anything and so could be defined here,
    but this then ceases to be an abstract class. Therefore
    _calculate_new_value() must be defined for each concrete implementation
    of this class, which is a bit of a bodge.
    """

    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Fix the specified attribute on the file
        """
        self._calculate_new_value()
        self._run_ncatted('d')


class RemoveHalo(NcoDataFix, metaclass=ABCMeta):
    """
    Remove the halo from in the HadGEM ORCA grids.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)
        self.row_spec = None

    @abstractmethod
    def _set_row_spec(self):
        """
        Specify the rows to be removed.
        """
        pass

    def apply_fix(self):
        """
        Remove the halo.
        """
        self._set_row_spec()
        self.command = f'ncks -h {self.row_spec}'
        self._run_nco_command(NcksError)


class MultiStageDataFix(DataFix, metaclass=ABCMeta):
    """
    A DataFix where intermediate files are generated by multiple intermediate
    commands. When an external command fails then these intermediate files are
    deleted.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)
        self.intermediate_files = []

    def _run_command(self, cmd, cmd_error):
        """
        Run `cmd` and raise `cmd_error` if it fails when the specified
        temporary files are deleted.

        :param str cmd: The command to run
        :param PreProcError cmd_error: The exception to raise if the command
            fails
        :param list temp_files: Intermediate files to delete if there's a
            problem
        """
        try:
            run_command(cmd)
        except Exception:
            for fn in self.intermediate_files:
                if os.path.exists(fn):
                    os.remove(fn)
            raise cmd_error(type(self).__name__, self.filename, cmd,
                            traceback.format_exc())


class FixHadGEMMask(MultiStageDataFix, metaclass=ABCMeta):
    """
    Fix the land sea mask in the HadGEM ORCA grids.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)
        self.byte_mask_file = None
        self.mask_var_name = None

    @abstractmethod
    def _set_byte_mask(self):
        """
        In concrete implementations, specify the byte_mask file and mask
        variable name here.
        """
        pass

    def apply_fix(self):
        """
        Add the byte mask, mask the relevant points and remove the mask.
        """
        self._set_byte_mask()
        # Make a temporary copy of the file that will be worked upon
        output_file = os.path.join(self.directory, self.filename)
        temp_file = output_file + '.temp'
        masked_file = output_file + '.temp_masked'
        final_file = output_file + '.temp_final'
        self.intermediate_files = [temp_file, masked_file, final_file]

        # Remove any temporary file left over from a previous failed
        # run as it could prevent some nco commands from running.
        for fn in self.intermediate_files:
            if os.path.exists(fn):
                os.remove(fn)
        shutil.copyfile(output_file, temp_file)

        # Copy the mask into the file
        command = (f"ncks -h -A -v {self.mask_var_name} {self.byte_mask_file} "
                   f"{temp_file}")
        self._run_command(command, NcksError)

        # Do the masking
        command = (f"ncap2 -h -s 'where({self.mask_var_name} != 0) "
                   f"{self.variable_name}={self.variable_name}@_FillValue' "
                   f"{temp_file} {masked_file}")
        self._run_command(command, Ncap2Error)

        # Remove the mask
        command = (f"ncks -h -x -v {self.mask_var_name} {masked_file} "
                   f"{final_file}")
        self._run_command(command, NcksError)

        # Set the name on the file and remove intermediate files
        os.remove(output_file)
        os.rename(final_file, output_file)
        self.intermediate_files.remove(final_file)
        for fn in self.intermediate_files:
            os.remove(fn)


class InsertHadGEMGrid(MultiStageDataFix, metaclass=ABCMeta):
    """
    Insert the correct grid into HadGEM ocean and ice files.
    """
    def __init__(self, filename, directory):
        """Initialise the class"""
        super().__init__(filename, directory)
        self.known_good_file = None

    def apply_fix(self):
        """
        Insert the correct grid. The file is first converted to netCDF3
        because the version 4 library has known bugs that prevent these
        operations.

        ncks -3 --no_alphabetize vo_Omon_HadGEM3-GC31-LL_hist-1950_r1i1p1f1_gn_195001-195012.nc vo.nc
        ncks -A -v latitude,longitude,vertices_latitude,vertices_longitude known_good.nc vo.nc
        rm vo_Omon_HadGEM3-GC31-LL_hist-1950_r1i1p1f1_gn_195001-195012.nc
        ncks -7 --deflate=3 vo.nc vo_Omon_HadGEM3-GC31-LL_hist-1950_r1i1p1f1_gn_195001-195012.nc
        """
        self._set_known_good()
        output_file = os.path.join(self.directory, self.filename)
        temp_file = output_file + '.temp'
        backup_file = output_file + '.temp_backup'
        self.intermediate_files = [temp_file, backup_file]

        if os.path.exists(temp_file):
            os.remove(temp_file)

        # Convert to netCDF3
        command = f'ncks -h -3 --no_alphabetize {output_file} {temp_file}'
        self._run_command(command, NcksError)

        # Paste in the grid
        command = (f'ncks -h -A -v latitude,longitude,vertices_latitude,'
                   f'vertices_longitude {self.known_good_file} {temp_file}')
        self._run_command(command, NcksError)

        # All's gone well so rename the original file
        os.rename(output_file, backup_file)

        # Save as netCDF v4
        command = f'ncks -h -7 --deflate=3 {temp_file} {output_file}'
        self._run_command(command, NcksError)

        # Complete so remove the intermediate files
        for fn in self.intermediate_files:
            os.remove(fn)

    @abstractmethod
    def _set_known_good(self):
        """
        In concrete implementations, specify the file containging the known
        good grid here.
        """
        pass
