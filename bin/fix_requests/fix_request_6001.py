#!/usr/bin/env python
"""
fix_request_6001.py

MOHC/NERC.HadGEM3-GC31-*.*.*.Amon/day/E3hrPt.[uv]a

Add cell_measures area: areacella to all MOHC and NERC Amon ua and va
variables.
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
    uva_reqs = DataRequest.objects.filter(
        institution_id__name__in=['MOHC', 'NERC'],
        table_id__in=['Amon', 'day'],
        cmor_name__in=['ua', 'va']
    )

    uva7h_reqs = DataRequest.objects.filter(
        institution_id__name__in=['MOHC', 'NERC'],
        table_id='E3hrPt',
        cmor_name__in=['ua7h', 'va7h']
    )

    data_reqs = uva_reqs | uva7h_reqs

    areacella = FileFix.objects.get(name='CellMeasuresAreacellaAdd')
    ext_vars = FileFix.objects.get(name='ExternalVariablesAreacella')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(areacella)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(areacella.name, data_reqs.count()))

    for data_req in uva7h_reqs:
        data_req.fixes.add(ext_vars)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(ext_vars.name, uva7h_reqs.count()))


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
