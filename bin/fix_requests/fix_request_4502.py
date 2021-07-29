#!/usr/bin/env python
"""
fix_request_4502.py

EC-Earth-Consortium.EC-Earth3P-HR.spinup-1950.r1i1p1f1.[O|SI]mon

cell_measures areacello cell_methods
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
    ### Cell Measures
    data_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        source_id__name='EC-Earth3P-HR',
        experiment_id__name='spinup-1950',
        variant_label='r1i1p1f1',
        table_id__in=['Omon', 'SImon', 'PrimOmon']
    )

    # Remove bad
    bad_fixes = [
        FileFix.objects.get(name='CellMeasuresAreacellaAdd'),
    ]

    for data_req in data_reqs:
        for fix in bad_fixes:
            data_req.fixes.remove(fix)

    num_data_reqs = data_reqs.count()
    for fix in bad_fixes:
        logger.debug('FileFix {} removed from {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Add good
    fixes = [
        FileFix.objects.get(name='CellMeasuresAreacelloAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ### Cell Methods (ocean only)
    data_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        source_id__name='EC-Earth3P-HR',
        experiment_id__name='spinup-1950',
        variant_label='r1i1p1f1',
        table_id__in=['Omon']
    )

    fixes = [
        FileFix.objects.get(name='CellMethodsSeaAreaTimeMeanAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))


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
