#!/usr/bin/env python
"""
fix_request_6010.py

HadGEM3-GC31-*.[O]fx

Correct nominal_resolution
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
    # N216 atmos
    data_reqs = DataRequest.objects.filter(
        source_id__name__in=['HadGEM3-GC31-MM', 'HadGEM3-GC31-MH'],
        table_id='fx',
    )

    nr100 = FileFix.objects.get(name='NominalResolution100km')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(nr100)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(nr100.name, data_reqs.count()))

    # N512 atmos
    data_reqs = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-HH',
        table_id='fx',
    )

    nr50 = FileFix.objects.get(name='NominalResolution50km')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(nr50)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(nr50.name, data_reqs.count()))

    # ORCA1 ocean
    data_reqs = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-LL',
        table_id='Ofx',
    )

    nr100 = FileFix.objects.get(name='NominalResolution100km')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(nr100)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(nr100.name, data_reqs.count()))

    # ORCA025 ocean
    data_reqs = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-MM',
        table_id='Ofx',
    )

    nr25 = FileFix.objects.get(name='NominalResolution25km')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(nr25)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(nr25.name, data_reqs.count()))

    # ORCA12 ocean
    data_reqs = DataRequest.objects.filter(
        source_id__name__in=['HadGEM3-GC31-MH', 'HadGEM3-GC31-HH'],
        table_id='Ofx',
    )

    nr10 = FileFix.objects.get(name='NominalResolution10km')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(nr10)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(nr10.name, data_reqs.count()))


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
