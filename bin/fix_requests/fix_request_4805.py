#!/usr/bin/env python
"""
fix_request_4805.py

EC-Earth-Consortium.EC-Earth3P.highres-future.r1i1p1f1.6hrPlevPt.zg7h

Don't fix var_name
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
    common_atributes = {
        'institution_id__name': 'EC-Earth-Consortium',
        'source_id__name': 'EC-Earth3P',
        'experiment_id__name': 'highres-future',
        'variant_label__regex': 'r1i1p1f1'
    }

    data_reqs = DataRequest.objects.filter(
        **common_atributes,
        table_id='6hrPlevPt',
        cmor_name='zg7h'
    )

    new_fixes = [
        FileFix.objects.get(name='AAVarNameToFileName'),
    ]

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables

    # Add new
    num_data_reqs = data_reqs.count()
    for data_req in data_reqs:
        for fix in new_fixes:
            data_req.remove.add(fix)

    for fix in new_fixes:
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
