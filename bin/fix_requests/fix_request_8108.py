#!/usr/bin/env python
"""
fix_request_8108.py

MPI-M.*.highresSST-*.*.6hrPlevPt.many

Set the cell_methods to "area: mean time: point" on various variables.
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
    sixhrplevpt = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__in=['highresSST-present', 'highresSST-future'],
        table_id='6hrPlevPt',
        cmor_name__in=[
            'hus7h', 'psl', 'ta7h', 'ua7h', 'uas', 'va7h', 'vas', 'zg7h'
        ]
    )

    data_reqs = sixhrplevpt

    cm_amtp = FileFix.objects.get(name='CellMethodsAreaMeanTimePointAdd')
    ext_vars = FileFix.objects.get(name='ExternalVariablesAreacella')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(cm_amtp)
        data_req.fixes.add(ext_vars)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(cm_amtp.name, data_reqs.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(ext_vars.name, data_reqs.count()))


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
