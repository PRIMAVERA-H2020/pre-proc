#!/usr/bin/env python
"""
fix_request_8002.py

MPI-M.many (except highresSST-present)

Add external_variables areacella.
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
    t_6hrPlev = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = '6hrPlev',
        cmor_name__in = ['wap4']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_6hrPlevPt = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = '6hrPlevPt',
        cmor_name__in = ['hus7h', 'psl', 'ta', 'ua', 'uas', 'va', 'vas', 'zg7h']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_Amon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Amon',
        cmor_name__in = ['cl', 'cli', 'clivi', 'clt', 'clw', 'clwvi',
                         'evspsbl', 'hfls', 'hfss', 'hur', 'hurs', 'hus',
                         'huss', 'pr', 'prc', 'prsn', 'prw', 'ps', 'psl',
                         'rlds', 'rldscs', 'rlus', 'rlut', 'rlutcs', 'rsds',
                         'rsdscs', 'rsdt', 'rsus', 'rsuscs', 'rsut', 'rsutcs',
                         'rtmt', 'sfcWind', 'ta', 'tas', 'tasmax', 'tasmin',
                         'tauu', 'tauv', 'ts', 'ua', 'uas', 'va', 'vas', 'wap',
                         'zg']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_Eday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Eday',
        cmor_name__in = ['tauu', 'tauv']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_LImon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'LImon',
        cmor_name__in = ['snw']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_Lmon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Lmon',
        cmor_name__in = ['mrso']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_Prim6hr = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Prim6hr',
        cmor_name__in = ['clt', 'hus4', 'pr', 'ps', 'rsds', 'ua4', 'va4']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_PrimSIday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'PrimSIday',
        cmor_name__in = ['siu', 'siv']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_Primday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'Primday',
        cmor_name__in = ['evspsbl', 'hus23', 'mrlsl', 'mrso', 'ta23', 'ts',
                         'ua23', 'va23', 'wap23', 'zg23']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_PrimdayPt = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'PrimdayPt',
        cmor_name__in = ['ua', 'va']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_SIday = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'SIday',
        cmor_name__in = ['sithick']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_SImon = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'SImon',
        cmor_name__in = ['sidconcdyn', 'sidconcth', 'sidmassdyn', 'sidmassth',
                         'sifb', 'siflcondbot', 'siflcondtop', 'siflfwbot',
                         'sihc', 'simass', 'sisaltmass', 'sisnconc', 'sisnhc',
                         'sisnmass', 'sisnthick', 'sispeed', 'sistrxubot',
                         'sistryubot', 'sithick', 'sitimefrac', 'sivol',
                         'sndmassdyn', 'sndmasssnf']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    t_day = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        table_id = 'day',
        cmor_name__in = ['clt', 'hfls', 'hfss', 'hur', 'hurs', 'hus', 'huss',
                         'pr', 'prc', 'prsn', 'psl', 'rlds', 'rlus', 'rlut',
                         'rsds', 'rsus', 'sfcWind', 'sfcWindmax', 'snw', 'ta',
                         'tas', 'tasmax', 'tasmin', 'ua', 'uas', 'va', 'vas',
                         'wap', 'zg']
    ).exclude(
        experiment_id__name='highresSST-present'
    )

    data_reqs = (t_6hrPlev | t_6hrPlevPt | t_Amon | t_Eday | t_LImon | t_Lmon |
                 t_Prim6hr | t_PrimSIday | t_Primday | t_PrimdayPt | t_SIday |
                 t_SImon | t_day)

    ext_var_cella = FileFix.objects.get(name='ExternalVariablesAreacella')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(ext_var_cella)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(ext_var_cella.name, data_reqs.count()))


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
