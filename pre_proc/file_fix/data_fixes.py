"""
data_fixes.py

Workers that edit the data in netCDF files that are based on the DataFix
abstract base class.
"""
import os
import traceback

from .abstract import DataFix
from pre_proc.common import run_command
from pre_proc.exceptions import NcpdqError


class LatDirection(DataFix):
    """
    Reverse the direction of the latitude dimension using ncpdq.
    """
    def __init__(self, filename, directory):
        """
        Initialise the class
        """
        super().__init__(filename, directory)

    def apply_fix(self):
        """
        Run ncpdq.
        """
        output_file = os.path.join(self.directory, self.filename)
        temp_file = output_file + '.temp'
        cmd = 'ncpdq -a -lat {} {}'.format(output_file, temp_file)
        try:
            run_command(cmd)
        except Exception:
            raise NcpdqError(type(self).__name__, self.filename, cmd,
                             traceback.format_exc())

        os.remove(output_file)
        os.rename(temp_file, output_file)
