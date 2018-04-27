#!/usr/bin/env python2.7
"""
fix_request_0005.py

Convert the further_info_url attribute on all EC-Earth data from HTTP to HTTPS.
Also, update branch_method and data_specs_version.

Add a few other fixes to EC-Earth Amon/tas and day/sfcWind data for the current
tests.
"""
import argparse
import logging.config
import sys

import django
django.setup()

from pre_proc_app.models import DataRequest, FileFix


__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Add pre-processing rules.')
    parser.add_argument('-l', '--log-level', help='set logging level to one '
                                                  'of debug, info, warn (the '
                                                  'default), or error')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    return args


def main():
    """
    Main entry point
    """
    data_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
    )

    further_info_https = FileFix.objects.get(name='FurtherInfoUrlToHttps')
    branch_method = FileFix.objects.get(name='BranchMethodAdd')
    data_specs = FileFix.objects.get(name='DataSpecsVersionAdd')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(further_info_https)
        data_req.fixes.add(branch_method)
        data_req.fixes.add(data_specs)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(further_info_https.name, data_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(branch_method.name, data_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(data_specs.name, data_reqs.count()))

    # update cell_methods and cell_measures on a single variable in
    # three experiments

    data_reqs_amip = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='highresSST-present',
        table_id='Amon',
        cmor_name='tas'
    )
    data_reqs_spinup = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='spinup-1950',
        source_id__name='EC-Earth3-HR',
        table_id='Amon',
        cmor_name='tas'
    )

    all_reqs = data_reqs_amip.union(data_reqs_spinup)

    cell_measures = FileFix.objects.get(name='CellMeasuresAreacellaAdd')
    cell_methods = FileFix.objects.get(name='CellMethodsAreaTimeMeanAdd')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in all_reqs:
        data_req.fixes.add(cell_measures)
        data_req.fixes.add(cell_methods)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(cell_measures.name, all_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(cell_methods.name, all_reqs.count()))

    # update three attributes on a single variable in
    # spinup-1950

    phys_index = FileFix.objects.get(name='PhysicsIndexIntFix')
    branch_time_parent = FileFix.objects.get(name='ParentBranchTimeDoubleFix')
    branch_time_child = FileFix.objects.get(name='ChildBranchTimeDoubleFix')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs_spinup:
        data_req.fixes.add(phys_index)
        data_req.fixes.add(branch_time_parent)
        data_req.fixes.add(branch_time_child)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(phys_index.name, all_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(branch_time_parent.name, all_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(branch_time_child.name, all_reqs.count()))

    # update cell_methods on day/sfcWind in
    # three experiments

    data_reqs_sfcWind = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='highresSST-present',
        table_id='day',
        cmor_name='sfcWind'
    )

    cell_methods = FileFix.objects.get(name='CellMethodsAreaTimeMeanAdd')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs_sfcWind:
        data_req.fixes.add(cell_methods)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(cell_methods.name, all_reqs.count()))


if __name__ == "__main__":
    cmd_args = parse_args()

    # determine the log level
    if cmd_args.log_level:
        try:
            log_level = getattr(logging, cmd_args.log_level.upper())
        except AttributeError:
            logger.setLevel(logging.WARNING)
            logger.error('log-level must be one of: debug, info, warn or error')
            sys.exit(1)
    else:
        log_level = DEFAULT_LOG_LEVEL

    # configure the logger
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': DEFAULT_LOG_FORMAT,
            },
        },
        'handlers': {
            'default': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': True
            }
        }
    })

    # run the code
    main()
