#!/usr/bin/env python
"""
fix_request_4606.py

EC-Earth-Consortium.EC-Earth3P(-HR).control-1950.r1i1p1f1.various

Set var_name to out_name
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
        'source_id__name__startswith': 'EC-Earth3P',
        'experiment_id__name': 'control-1950',
        'variant_label__regex': 'r1i1p1f1'
    }

    six_hour_plev = DataRequest.objects.filter(
        **common_atributes,
        table_id='6hrPlev',
        cmor_name='wap4'
    )

    six_hour_plev_pt = DataRequest.objects.filter(
        **common_atributes,
        table_id='6hrPlevPt',
        cmor_name__in=['hus7h', 'ta7h', 'ua7h', 'va7h', 'zg7h']
    )

    emon = DataRequest.objects.filter(
        **common_atributes,
        table_id='Emon',
        cmor_name__in=['hus27', 'ta27', 'ua27', 'va27', 'zg27']
    )

    omon = DataRequest.objects.filter(
        **common_atributes,
        table_id='Omon',
        cmor_name='ficeberg2d'
    )

    data_reqs = six_hour_plev | six_hour_plev_pt | emon | omon

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
