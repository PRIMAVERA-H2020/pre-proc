#!/usr/bin/env python
"""
fix_request_6403.py

MOHC.ocean_ORCA1.*

In all MOHC coupled data on the ORCA1 grid remove the halo.
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
        source_id__name='HadGEM3-GC31-LL',
        table_id__in=['Oday', 'PrimOday', 'Omon', 'PrimOmon', 'Ofx']
    )

    # Add fix
    fixes = [
        FileFix.objects.get(name='AAARemoveOrca1Halo'),
    ]

    for data_req in data_reqs:
        data_req.fixes.add(*fixes)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Remove fix with old name
    fixes = [
        FileFix.objects.get(name='RemoveOrca1Halo'),
    ]

    for data_req in data_reqs:
        data_req.fixes.remove(*fixes)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} removed from {} data requests.'.
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
