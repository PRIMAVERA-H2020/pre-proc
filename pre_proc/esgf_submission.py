"""
esgf_sumbission.py

The basic class that forms an ESGF submission
"""
import os

from pre_proc.file_fix import ParentBranchTimeDoubleFix, ChildBranchTimeDoubleFix


class EsgfSubmission(object):
    """
    The basic class that forms an ESGF submission
    """
    def __init__(self, source_id=None, experiment_id=None, table_id=None,
                 cmor_name=None, filepath=None):
        """
        Initialise the class.

        :param str source_id: The CMIP6 source_id
        :param str experiment_id: The CMIP6 experiment_id
        :param str table_id: The CMIP6 table_id
        :param str cmor_name: The CMIP6 cmor_name
        :param str filepath: The full path to the file to be fixed.
        """
        self.source_id = source_id
        self.experiment_id = experiment_id
        self.table_id = table_id
        self.cmor_name = cmor_name
        self.filename = os.path.basename(filepath)
        self.directory = os.path.dirname(filepath)
        self.fixes = []

    @classmethod
    def from_file(cls, filepath):
        """
        Create a submission from a specified file.

        :param str filepath: The file's full path.
        """
        components = ['cmor_name', 'table_id', 'source_id', 'experiment_id']
        basename_cmpts = os.path.basename(filepath).split('_')
        kwargs = {}
        for cmpt_name, cmpt in zip(components, basename_cmpts):
            kwargs[cmpt_name] = cmpt

        kwargs['filepath'] = filepath

        return cls(**kwargs)

    def determine_fixes(self):
        """
        Scan through the DB, determine the fixes that need to be run on
        this ESGF dataset and add them to the list
        """
        self.fixes.append(ParentBranchTimeDoubleFix(self.filename,
                                                    self.directory))
        self.fixes.append(ChildBranchTimeDoubleFix(self.filename,
                                                   self.directory))

    def run_fixes(self):
        """
        Loop through the fixes and run each of them in turn
        """
        for fix in self.fixes:
            fix.apply_fix()
