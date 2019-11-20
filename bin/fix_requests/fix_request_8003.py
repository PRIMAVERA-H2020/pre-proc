#!/usr/bin/env python
"""
fix_request_8003.py

MPI-M.many (except highresSST-present)

Add external_variables areacello.
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
    t_Oday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Oday',
        cmor_name__in = ['omldamax', 'sos', 'tos', 'tossq']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_Omon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Omon',
        cmor_name__in = ['fsitherm', 'hfds', 'hfx', 'hfy', 'mlotst',
                         'mlotstsq', 'msftbarot', 'pbo', 'rsntds', 'sfdsi',
                         'sos', 'tos', 'tossq', 'wfo', 'zos', 'zossq']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_PrimOday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'PrimOday',
        cmor_name__in = ['mlotst', 'zos']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_PrimOmon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'PrimOmon',
        cmor_name__in = ['opottemptend', 'somint', 'tomint', 'u2o', 'uso',
                         'uto', 'v2o', 'vso', 'vto', 'w2o', 'wo', 'wso', 'wto']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_PrimSIday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'PrimSIday',
        cmor_name__in = ['simassacrossline', 'sistrxdtop', 'sistrxubot',
                         'sistrydtop', 'sistryubot', 'sitimefrac']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_SIday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'SIday',
        cmor_name__in = ['siconc']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_SImon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'SImon',
        cmor_name__in = ['siconc']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    data_reqs = (t_Oday | t_Omon | t_PrimOday | t_PrimOmon | t_PrimSIday |
                 t_SIday | t_SImon)

    ext_var_cello = FileFix.objects.get(name='ExternalVariablesAreacello')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(ext_var_cello)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(ext_var_cello.name, data_reqs.count()))


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
