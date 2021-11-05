#!/usr/bin/env python
"""
fix_request_3901.py

CNRM-CERFACS.primWP5.assorted

CERFACS WP5 assorted specific variable fixes
"""
import argparse
import logging.config
import sys

import django
django.setup()

from pre_proc_app.models import DataRequest, FileFix  # noqa


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
    # Efx and fx external_variables areacella
    data_reqs = DataRequest.objects.filter(
        institution_id__name='CNRM-CERFACS',
        experiment_id__name__startswith='primWP5-amv',
        table_id__in=['Efx', 'fx'],
        cmor_name__in=['mrsofc', 'orog', 'rootd', 'sftgif', 'sftgrf', 'sftlf',
                       'zfull']
    )

    fixes = [
        FileFix.objects.get(name='ExternalVariablesAreacella'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Ofx external_variables areacello
    data_reqs = DataRequest.objects.filter(
        institution_id__name='CNRM-CERFACS',
        experiment_id__name__startswith='primWP5-amv',
        table_id='Ofx',
        cmor_name__in=['deptho', 'hfgeou']
    )

    fixes = [
        FileFix.objects.get(name='ExternalVariablesAreacello'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Ofx external_variables areacello volcello
    data_reqs = DataRequest.objects.filter(
        institution_id__name='CNRM-CERFACS',
        experiment_id__name__startswith='primWP5-amv',
        table_id='Ofx',
        cmor_name__in=['masscello', 'thkcello']
    )

    fixes = [
        FileFix.objects.get(name='ExternalVariablesAreacelloVolcello'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    # Ofx basin
    data_reqs = DataRequest.objects.filter(
        institution_id__name='CNRM-CERFACS',
        experiment_id__name__startswith='primWP5-amv',
        table_id='Ofx',
        cmor_name='basin'
    )

    fixes = [
        FileFix.objects.get(name='FillValueNeg999'),
        FileFix.objects.get(name='MissingValueNeg999'),
    ]

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
