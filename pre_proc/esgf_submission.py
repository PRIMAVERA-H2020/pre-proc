"""
esgf_sumbission.py

The basic class that forms an ESGF submission.
"""
import datetime
import logging
import os

from netCDF4 import Dataset

import django
import django.core.exceptions

django.setup()

import pre_proc
from pre_proc.common import run_command
from pre_proc.exceptions import DataRequestNotFound, MultipleDataRequestsFound
from pre_proc_app.models import DataRequest


logger = logging.getLogger(__name__)


class EsgfSubmission(object):
    """
    The basic class that forms an ESGF submission.
    """
    def __init__(self, source_id=None, experiment_id=None, variant_label=None,
                 table_id=None, cmor_name=None, filepath=None):
        """
        Initialise the class.

        :param str source_id: The CMIP6 source_id
        :param str experiment_id: The CMIP6 experiment_id
        :param str variant_label: The CMIP6 variant_label
        :param str table_id: The CMIP6 table_id
        :param str cmor_name: The CMIP6 cmor_name
        :param str filepath: The full path to the file to be fixed
        """
        self.source_id = source_id
        self.experiment_id = experiment_id
        self.variant_label = variant_label
        self.table_id = table_id
        self.cmor_name = cmor_name
        self.filename = os.path.basename(filepath)
        self.directory = os.path.dirname(filepath)
        self.fixes = []

    @classmethod
    def from_file(cls, filepath):
        """
        Create a submission from a specified file.

        :param str filepath: The file's full path
        :returns: An EsgfSubmission object initialised from the specified
            file
        :rtype: pre_proc.EsgfSubmission
        """
        components = ['cmor_name', 'table_id', 'source_id', 'experiment_id',
                      'variant_label']
        basename_cmpts = os.path.basename(filepath).split('_')
        kwargs = {}
        for cmpt_name, cmpt in zip(components, basename_cmpts):
            kwargs[cmpt_name] = cmpt

        kwargs['filepath'] = filepath

        return cls(**kwargs)

    def determine_fixes(self):
        """
        Scan through the DB, determine the fixes that need to be run on
        this ESGF dataset and add them to the list.
        """
        self.fixes = [getattr(pre_proc.file_fix, fix_name.name)(self.filename,
                                                                self.directory)
                      for fix_name in self._get_data_request().fixes.all()]

    def run_fixes(self):
        """
        Loop through the fixes and run each of them in turn.
        """
        for fix in self.fixes:
            fix.apply_fix()

    def update_history(self):
        """
        Add the fixes run to the history attribute.
        """
        fix_names = [fix.__class__.__name__ for fix in self.fixes]
        fix_names.sort()
        filepath = os.path.join(self.directory, self.filename)

        time_now = datetime.datetime.utcnow().replace(microsecond=0)
        filefix_history = '{}Z {}'.format(time_now.isoformat(),
                                          ', '.join(fix_names))

        existing_history = _get_attribute(filepath, 'history')
        if existing_history:
            new_history = '{}; {}'.format(existing_history, filefix_history)
        else:
            new_history = filefix_history

        _set_attribute(filepath, 'history', new_history)

    def _get_data_request(self):
        """
        Return the DataRequest object from the database that corresponds to
        this ESGF submission.

        :returns: the data request object corresponding to this submission
        :rtype: pre_proc_app.models.DataRequest
        """
        try:
            dreq = DataRequest.objects.get(
                source_id__name=self.source_id,
                experiment_id__name=self.experiment_id,
                variant_label=self.variant_label,
                table_id=self.table_id,
                cmor_name=self.cmor_name
            )
        except django.core.exceptions.ObjectDoesNotExist:
            try:
                dreq = DataRequest.objects.get(
                    source_id__name=self.source_id,
                    experiment_id__name=self.experiment_id,
                    variant_label=self.variant_label,
                    table_id=self.table_id,
                    cmor_name__startswith=self.cmor_name
                )
            except django.core.exceptions.ObjectDoesNotExist:
                raise DataRequestNotFound(self.directory, self.filename)
            except django.core.exceptions.MultipleObjectsReturned:
                raise MultipleDataRequestsFound(self.directory, self.filename)

        return dreq


def _get_attribute(filepath, attr_name):
    """
    Return the specified global attribute value from the specified file.

    :param str filepath: The name of the netCDF file to load
    :param str attr_name: The name of the attribute to get
    :returns: The value of the specified attribute, None is it doesn't exist
    :rtype: str
    :raises RunTimeError: if unable to open the file
    """
    try:
        with Dataset(filepath) as rootgrp:
            attr_value = getattr(rootgrp, attr_name, None)
    except IOError:
        msg = 'Unable to open file {}'.format(filepath)
        logger.warning(msg)
        raise RuntimeError(msg)

    return attr_value


def _set_attribute(filepath, attr_name, attr_value):
    """
    Overwrite the specified global attribute value on the specified netCDF
    file.

    :param str filepath: The name of the netCDF file to update
    :param str attr_name: The name of the attribute to set
    :param str attr_value: The new value of the specified attribute
    :raises RunTimeError: if ncatted doesn't complete successfully
    """
    cmd = "ncatted -h -a {},global,o,c,'{}' {}".format(attr_name, attr_value,
                                                       filepath)
    run_command(cmd)
