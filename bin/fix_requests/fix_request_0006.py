#!/usr/bin/env python2.7
"""
fix_request_0006.py

Fix some AWI data. Convert the further_info_url attribute on all AWI data
from HTTP to HTTPS.
Fix additional items for variable Omon/so and Omon/tos.
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
        institution_id__name='AWI',
    )

    further_info = FileFix.objects.get(
        name='FurtherInfoUrlAWISourceIdAndHttps'
    )

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs:
        data_req.fixes.add(further_info)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(further_info.name, data_reqs.count()))

    # update cell_methods on day/sfcWind in
    # three experiments

    data_reqs_so = DataRequest.objects.filter(
        institution_id__name='AWI',
        experiment_id__name__in=['spinup-1950', 'hist-1950', 'control-1950'],
        table_id='Omon',
        cmor_name='so'
    )

    data_reqs_tos = DataRequest.objects.filter(
        institution_id__name='AWI',
        experiment_id__name__in=['spinup-1950', 'hist-1950', 'control-1950'],
        table_id='Omon',
        cmor_name='tos'
    )

    data_reqs_common = data_reqs_so.union(data_reqs_tos)

    parent_branch_time = FileFix.objects.get(name='ParentBranchTimeDoubleFix')
    child_branch_time = FileFix.objects.get(name='ChildBranchTimeDoubleFix')
    r_fix = FileFix.objects.get(name='RealizationIndexIntFix')
    i_fix = FileFix.objects.get(name='InitializationIndexIntFix')
    p_fix = FileFix.objects.get(name='PhysicsIndexIntFix')
    f_fix = FileFix.objects.get(name='ForcingIndexIntFix')
    parent_source_id = FileFix.objects.get(name='ParentSourceIdFromSourceId')
    salinity = FileFix.objects.get(name='SeaWaterSalinityStandardNameAdd')
    sea_temp = FileFix.objects.get(name='SeaSurfaceTemperatureNameAdd')
    cell_methdods = FileFix.objects.get(name='CellMethodsSeaAreaTimeMeanAdd')
    cell_measures_areavol = FileFix.objects.get(name='CellMeasuresAreacelloVolcelloAdd')
    cell_measures_area = FileFix.objects.get(name='CellMeasuresAreacelloAdd')
    var_units = FileFix.objects.get(name='VarUnitsToThousandths')
    fill_value = FileFix.objects.get(name='FillValueFromMissingValue')

    # This next line could be done more quickly by:
    # further_info_url_fix.datarequest_set.add(*data_reqs)
    # but sqlite3 gives an error of:
    # django.db.utils.OperationalError: too many SQL variables
    for data_req in data_reqs_common:
        data_req.fixes.add(parent_branch_time)
        data_req.fixes.add(child_branch_time)
        data_req.fixes.add(r_fix)
        data_req.fixes.add(i_fix)
        data_req.fixes.add(p_fix)
        data_req.fixes.add(f_fix)
        data_req.fixes.add(parent_source_id)
        data_req.fixes.add(cell_methdods)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(parent_branch_time.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(child_branch_time.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(r_fix.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(i_fix.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(p_fix.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(f_fix.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(parent_source_id.name, data_reqs_common.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(cell_methdods.name, data_reqs_common.count()))

    for data_req in data_reqs_so:
        data_req.fixes.add(salinity)
        data_req.fixes.add(cell_measures_areavol)
        data_req.fixes.add(var_units)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(salinity.name, data_reqs_so.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(cell_measures_areavol.name, data_reqs_so.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(var_units.name, data_reqs_so.count()))

    for data_req in data_reqs_tos:
        data_req.fixes.add(sea_temp)
        data_req.fixes.add(cell_measures_area)
        data_req.fixes.add(fill_value)

    logger.debug('FileFix {} added to {} data requests.'.
                 format(sea_temp.name, data_reqs_tos.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(cell_measures_area.name, data_reqs_tos.count()))
    logger.debug('FileFix {} added to {} data requests.'.
                 format(fill_value.name, data_reqs_tos.count()))


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
