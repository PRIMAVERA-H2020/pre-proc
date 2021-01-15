#!/usr/bin/env python
"""
fix_request_4802.py

EC-Earth-Consortium.EC-Earth3P(-HR).highres-future.r1i1p1f1.3hr.tos

Convert from atmos to ocean
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
        source_id__name__startswith='EC-Earth3P',
        experiment_id__name='highres-future',
        variant_label__regex='r1i1p1f1',
        table_id='3hr',
        cmor_name='tos'
    )

    bad_fixes = [
        FileFix.objects.get(name='ZZEcEarthAtmosFix'),
        FileFix.objects.get(name='ZZZEcEarthLongitudeFix')
    ]

    new_fixes = [
        FileFix.objects.get(name='RealmOcean'),
        FileFix.objects.get(name='ExternalVariablesAreacello')
    ]

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables

    # Remove bad
    for data_req in data_reqs:
        for fix in bad_fixes:
            data_req.fixes.remove(fix)

    num_data_reqs = data_reqs.count()
    for fix in bad_fixes:
        logger.debug('FileFix {} removed from {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Add new
    for data_req in data_reqs:
        for fix in new_fixes:
            data_req.fixes.add(fix)

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
