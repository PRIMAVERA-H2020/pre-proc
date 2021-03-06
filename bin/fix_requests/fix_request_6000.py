#!/usr/bin/env python
"""
fix_request_6000.py

MOHC.*

Convert the further_info_url attribute on all MOHC and NERC data from HTTP to
HTTPS. Update data_specs_version to 01.00.23.
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
        institution_id__name__in=['MOHC', 'NERC']
    ).exclude(
        source_id__name='HadGEM3-GC31-HH',
        experiment_id__name__in=['control-1950', 'hist-1950']
    )

    further_info_url_fix = FileFix.objects.get(name='FurtherInfoUrlToHttps')
    data_specs = FileFix.objects.get(name='DataSpecsVersionAdd')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(further_info_url_fix)
        data_req.fixes.add(data_specs)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(further_info_url_fix.name, data_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(data_specs.name, data_reqs.count()))

    # Remove from existing -HH
    data_reqs = DataRequest.objects.filter(
        source_id__name='HadGEM3-GC31-HH',
        experiment_id__name__in=['control-1950', 'hist-1950']
    )
    for data_req in data_reqs:
        data_req.fixes.remove(further_info_url_fix)

    logger.debug('FileFix {} removed from {} data requests.'.
                 format(further_info_url_fix.name, data_reqs.count()))

    # But add the data_spec fix back in
    data_reqs = DataRequest.objects.filter(
        institution_id__name__in=['MOHC', 'NERC'],
        source_id__name='HadGEM3-GC31-HH',
        experiment_id__name__in=['control-1950', 'hist-1950']
    )

    data_specs = FileFix.objects.get(name='DataSpecsVersionAdd')

    for data_req in data_reqs:
        data_req.fixes.add(data_specs)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(data_specs.name, data_reqs.count()))


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
