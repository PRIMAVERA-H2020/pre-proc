#!/usr/bin/env python
"""
fix_request_5901.py

ECMWF.primWP5.assorted

ECMWF WP5 assorted specific variable fixes
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
    ## evspsbl
    data_reqs = DataRequest.objects.filter(
        institution_id__name='ECMWF',
        experiment_id__name__startswith='primWP5-amv',
        cmor_name='evspsbl'
    )

    fixes = [
        FileFix.objects.get(name='EvapotranspirationNameAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ## mrso
    data_reqs = DataRequest.objects.filter(
        institution_id__name='ECMWF',
        experiment_id__name__startswith='primWP5-amv',
        cmor_name='mrso'
    )

    fixes = [
        FileFix.objects.get(name='SoilMoistureNameAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ## psl
    data_reqs = DataRequest.objects.filter(
        institution_id__name='ECMWF',
        experiment_id__name__startswith='primWP5-amv',
        cmor_name='psl'
    )

    fixes = [
        FileFix.objects.get(name='PressureNameAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))


    ## sithick
    data_reqs = DataRequest.objects.filter(
        institution_id__name='ECMWF',
        experiment_id__name__startswith='primWP5-amv',
        cmor_name='sithick'
    )

    fixes = [
        FileFix.objects.get(name='ExternalVariablesAreacello'),
        FileFix.objects.get(name='CellMeasuresAreacelloAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ## tos
    data_reqs = DataRequest.objects.filter(
        institution_id__name='ECMWF',
        experiment_id__name__startswith='primWP5-amv',
        cmor_name='tos'
    )

    fixes = [
        FileFix.objects.get(name='ToDegC'),
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
