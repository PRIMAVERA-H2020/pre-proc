#!/usr/bin/env python
"""
fix_request_6447.py

HadGEM3-GC31*.ice_ORCA.selected

For variables with a bug in the cell_methods in version 01.00.23 of the tables
update the tables to 01.00.29.
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
    """Main entry point"""
    data_reqs = DataRequest.objects.filter(
        source_id__name__startswith='HadGEM3-GC31',
        table_id='SImon',
        cmor_name__in=['sidmassdyn', 'sidmassmeltbot', 'sidmassmelttop',
                       'sidmassth', 'siflsaltbot', 'sihc', 'simass',
                       'sisnthick', 'sitimefrac', 'sivol']
    ).exclude(
        source_id__name='HadGEM3-GC31-HH'
    )

    old_fixes = [
        FileFix.objects.get(name='DataSpecsVersionAdd'),
    ]

    new_fixes = [
        FileFix.objects.get(name='DataSpecsVersion29Add'),
    ]

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        for fix in old_fixes:
            data_req.fixes.remove(fix)

    num_data_reqs = data_reqs.count()
    for fix in old_fixes:
        logger.debug('FileFix {} removed from {} data requests.'.
                     format(fix.name, num_data_reqs))

    for data_req in data_reqs:
        data_req.fixes.add(*new_fixes)

    num_data_reqs = data_reqs.count()
    for fix in new_fixes:
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
