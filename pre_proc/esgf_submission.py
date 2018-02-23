"""
esgf_sumbission.py

The basic class that forms an ESGF submission
"""
class EsgfSubmission(object):
    """
    The basic class that forms an ESGF submission
    """
    def __init__(self, institution_id, source_id, experiment_id, table_id,
                 cmor_name):
        """
        Initialise the class

        :param str institution_id: The CMIP6 institution_id
        :param str source_id: The CMIP6 source_id
        :param str experiment_id: The CMIP6 experiment_id
        :param str table_id: The CMIP6 table_id
        :param str cmor_name: The CMIP6 cmor_name
        """
        self.institution = institution_id
        self.source_id = source_id
        self.experiment_id = experiment_id
        self.table_id = table_id
        self.cmor_name = cmor_name
        self.fixes = []

    def determine_fixes(self):
        """
        Scan through the DB, determine the fixes that need to be run on
        this ESGF dataset and add them to the list
        """
        pass

    def run_fixes(self):
        """
        Loop through the fixes and run each of them in turn
        """
        pass
