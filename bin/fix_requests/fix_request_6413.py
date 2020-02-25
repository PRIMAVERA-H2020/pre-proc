#!/usr/bin/env python
"""
fix_request_6413.py

MOHC.ice_ORCA1_grid-t.*

In all MOHC ice data on the ORCA1 t-grid fix the coordinates.
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
    simon = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-LL',
        table_id='SImon',
        cmor_name__in=['siage', 'sidmassdyn', 'sidmassmeltbot',
                       'sidmassmelttop', 'sidmassth', 'siflcondbot',
                       'siflcondtop', 'siflfwbot', 'siflfwdrain',
                       'sifllatstop', 'siflsaltbot', 'siflsensupbot', 'sihc',
                       'simass', 'sipr', 'sisnconc', 'sisnhc', 'sisnmass',
                       'sisnthick', 'sitempbot', 'sithick', 'sitimefrac',
                       'sivol']
    )

    siday = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-LL',
        table_id='SIday',
        cmor_name__in=['sithick']
    )

    primsiday = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-LL',
        table_id='SIday',
        cmor_name__in=['sitimefrac']
    )

    data_reqs = (simon | siday | primsiday)

    fixes = [
        FileFix.objects.get(name='FixCiceCoords1T'),
    ]

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(*fixes)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Remove this fix from siconc where it may have previously been erroneously
    # added.
    siconc = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-LL',
        table_id__in=['SIday', 'SImon'],
        cmor_name='siconc'
    )

    for data_req in siconc:
        data_req.fixes.remove(FileFix.objects.get(name='FixCiceCoords1T'))

    num_data_reqs = siconc.count()
    logger.debug('FileFix {} removed from {} data requests.'.
                 format(FileFix.objects.get(name='FixCiceCoords1T').name,
                        num_data_reqs))



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
