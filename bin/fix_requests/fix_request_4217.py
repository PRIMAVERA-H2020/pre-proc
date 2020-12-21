#!/usr/bin/env python
"""
fix_request_4217.py

EC-Earth-Consortium.EC-Earth3P-HR.highresSST-present.r1i1p1f1.6hrPlevPt.zg27

Create data request and set fixes.
"""
import argparse
import logging.config
import sys

import django
django.setup()

from pre_proc_app.models import (ClimateModel, DataRequest, Experiment,
                                 FileFix, Institution)


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
    ec_earth = Institution.objects.get(name='EC-Earth-Consortium')
    ec_earth3_hr = ClimateModel.objects.get(name='EC-Earth3P-HR')
    amip = Experiment.objects.get(name='highresSST-present')
    data_req = DataRequest.objects.create(
        institution_id=ec_earth,
        source_id=ec_earth3_hr,
        experiment_id=amip,
        variant_label='r1i1p1f1',
        table_id='6hrPlevPt',
        cmor_name='zg27'
    )

    fixes = [
        FileFix.objects.get(name='AAVarNameToFileName'),
        FileFix.objects.get(name='BranchTimeDelete'),
        FileFix.objects.get(name='CellMethodsAreaMeanTimePointAdd'),
        FileFix.objects.get(name='DataSpecsVersionAdd'),
        FileFix.objects.get(name='EcEarthInstitution'),
        FileFix.objects.get(name='HistoryClearOld'),
        FileFix.objects.get(name='ZZEcEarthAtmosFix'),
        FileFix.objects.get(name='ZZZEcEarthLongitudeFix'),
    ]

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for fix in fixes:
        data_req.fixes.add(fix)

    num_data_reqs = 1
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
