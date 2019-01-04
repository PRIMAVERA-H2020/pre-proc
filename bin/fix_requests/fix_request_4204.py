#!/usr/bin/env python
"""
fix_request_4204.py

EC-Earth-Consortium.*.highresSST-present.r1i1p1f1.*mon.many

Set the cell_measures.
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
    amon_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='highresSST-present',
        variant_label='r1i1p1f1',
        table_id='Amon',
        cmor_name__in=['clivi', 'clt', 'clwvi', 'evspsbl', 'hfls', 'hfss',
                       'hur', 'hus', 'pr', 'prc', 'prsn', 'prw', 'ps', 'psl',
                       'rlds', 'rldscs', 'rlus', 'rlut', 'rlutcs', 'rsds',
                       'rsdscs', 'rsdt', 'rsus', 'rsuscs', 'rsut', 'rsutcs',
                       'sbl', 'ta', 'tasmax', 'tasmin', 'tauu', 'tauv', 'ts',
                       'ua', 'va', 'wap', 'zg']
    )

    emon_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='highresSST-present',
        variant_label='r1i1p1f1',
        table_id='Emon',
        cmor_name__in=['hus27', 'ta27', 'ua27', 'va27', 'zg27']
    )

    limon_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='highresSST-present',
        variant_label='r1i1p1f1',
        table_id='LImon',
        cmor_name__in=['hfdsn', 'lwsnl', 'sbl', 'snc', 'snd', 'snm', 'snw',
                       'tsn']
    )

    lmon_reqs = DataRequest.objects.filter(
        institution_id__name='EC-Earth-Consortium',
        experiment_id__name='highresSST-present',
        variant_label='r1i1p1f1',
        table_id='Lmon',
        cmor_name__in=['evspsblsoi', 'mrro', 'mrros', 'mrso', 'mrsos', 'tsl']
    )

    data_reqs = amon_reqs | emon_reqs | limon_reqs | lmon_reqs

    fixes = [
        FileFix.objects.get(name='CellMeasuresAreacellaAdd')
    ]

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
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
