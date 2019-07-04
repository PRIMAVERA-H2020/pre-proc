"""
test_esgf_submission.py

Test the ESGFSubmission class.
"""
import datetime
import unittest
from unittest import mock

from pre_proc import EsgfSubmission
from pre_proc.file_fix import ChildBranchTimeAdd


class TestEsgfSubmission(unittest.TestCase):
    """ test esgf_submission.EsgfSubmission """
    def setUp(self):
        self.esgf = EsgfSubmission(source_id='source_id',
                                   experiment_id='experiment_id',
                                   variant_label='variant_label',
                                   table_id='table_id', cmor_name='cmor_name',
                                   filepath='/file/path')

        patch = mock.patch('pre_proc.esgf_submission._get_attribute')
        self.mock_get_attr = patch.start()
        self.mock_get_attr.return_value = None
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.esgf_submission._set_attribute')
        self.mock_set_attr = patch.start()
        self.addCleanup(patch.stop)

        patch = mock.patch('pre_proc.esgf_submission.datetime')
        self.mock_datetime = patch.start()
        self.mock_datetime.datetime.utcnow.return_value = (
            datetime.datetime(2000, 1, 1, 0, 0, 0)
        )
        self.addCleanup(patch.stop)

    def test_history_updated(self):
        """ Test that the history's updated """
        self.esgf.fixes.append(ChildBranchTimeAdd(self.esgf.filename,
                                                  self.esgf.directory))
        self.esgf.update_history()
        self.mock_set_attr.assert_called_once_with('/file/path', 'history',
                                                   '2000-01-01T00:00:00Z '
                                                   'ChildBranchTimeAdd')

    def test_no_fixes_no_history(self):
        """
        Test that no change is made to the history if no fixes have been
        applied.
        """
        self.esgf.update_history()
        self.mock_get_attr.assert_not_called()
        self.mock_set_attr.assert_not_called()
