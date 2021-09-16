#!/usr/bin/env python
"""
fix_request_8900.py

MPI-M.DCPP.*

Fix MPI WP5 files appropriately.
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
    ######################
    # Remove some existing
    ######################
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv'
    )

    fixes = [
        FileFix.objects.get(name='DataSpecsVersionAdd'),
        FileFix.objects.get(name='ParentBranchTime45655Add'),
        FileFix.objects.get(name='ChildBranchTime36524Add'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.remove(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} removed from {} data requests.'.
                     format(fix.name, num_data_reqs))

    ##############
    # All datasets
    ##############
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv'
    )

    fixes = [
        FileFix.objects.get(name='DataSpecsVersion27Add'),
        FileFix.objects.get(name='Conventions'),
        FileFix.objects.get(name='CreationDate201807'),
        FileFix.objects.get(name='RealizationIndexFromFilename'),
        FileFix.objects.get(name='InitializationIndexFromFilename'),
        FileFix.objects.get(name='PhysicsIndexFromFilename'),
        FileFix.objects.get(name='ForcingIndexFromFilename'),
        FileFix.objects.get(name='VariantLabelFromFilename'),
        FileFix.objects.get(name='GridLabelGnAdd'),
        FileFix.objects.get(name='GridNativeAdd'),
        FileFix.objects.get(name='MpiInstitution'),
        FileFix.objects.get(name='LicenseAdd'),
        FileFix.objects.get(name='ParentActIdAdd'),
        FileFix.objects.get(name='ParentExptIdCtrlAdd'),
        FileFix.objects.get(name='ParentMipEraAdd'),
        FileFix.objects.get(name='ParentTimeUnits1850Add'),
        FileFix.objects.get(name='BranchMethodStandardAdd'),
        FileFix.objects.get(name='ParentVariantLabel'),
        FileFix.objects.get(name='ProductAdd'),
        FileFix.objects.get(name='SourceTypeAogcmAdd'),
        FileFix.objects.get(name='SubExperiment'),
        FileFix.objects.get(name='SubExperimentId'),
        FileFix.objects.get(name='TableIdAdd'),
        FileFix.objects.get(name='TrackingIdNew'),
        FileFix.objects.get(name='VariableIdAdd'),
        FileFix.objects.get(name='ZFurtherInfoUrl'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ###############
    # dcppc-amv-neg
    ###############
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv-neg'
    )

    fixes = [
        FileFix.objects.get(name='DcppcAmvNegExpt'),
        FileFix.objects.get(name='DcppcAmvNegExptId'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ###############
    # dcppc-amv-pos
    ###############
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name='dcppc-amv-pos'
    )

    fixes = [
        FileFix.objects.get(name='DcppcAmvPosExpt'),
        FileFix.objects.get(name='DcppcAmvPosExptId'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    #######
    # daily
    #######
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv',
        table_id__contains='day'
    )

    fixes = [
        FileFix.objects.get(name='FrequencyDayAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    #########
    # monthly
    #########
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv',
        table_id__contains='mon'
    )

    fixes = [
        FileFix.objects.get(name='FrequencyMonAdd'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ###############
    # MPI-ESM1-2-HR
    ###############
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        source_id__name='MPI-ESM1-2-HR',
        experiment_id__name__startswith='dcppc-amv'
    )

    fixes = [
        FileFix.objects.get(name='NominalResolution100km'),
        FileFix.objects.get(name='MPIParentSourceIdHr'),
        FileFix.objects.get(name='MPISourceHr'),
        FileFix.objects.get(name='MPISourceIdHr')
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ###############
    # MPI-ESM1-2-XR
    ###############
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        source_id__name='MPI-ESM1-2-XR',
        experiment_id__name__startswith='dcppc-amv'
    )

    fixes = [
        FileFix.objects.get(name='NominalResolution50km'),
        FileFix.objects.get(name='MPIParentSourceIdXr'),
        FileFix.objects.get(name='MPISourceXr'),
        FileFix.objects.get(name='MPISourceIdXr')
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    #######
    # Atmos
    #######
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv'
    ).exclude(
        table_id__in=['Omon', 'SImon']
    )

    fixes = [
        FileFix.objects.get(name='RealmAtmos'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    #######
    # Ocean
    #######
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv',
        table_id='Omon'
    )

    fixes = [
        FileFix.objects.get(name='RealmOcean'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    #########
    # Sea Ice
    #########
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv',
        table_id='SImon'
    )

    fixes = [
        FileFix.objects.get(name='RealmSeaIce'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))

    ##########
    # r1i1p1f1
    ##########
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv',
        variant_label='r1i1p1f1'
    )

    fixes = [
        FileFix.objects.get(name='ChildBranchTime38714Add'),
        FileFix.objects.get(name='ParentBranchTime38714Add'),
    ]

    for data_req in data_reqs:
        for fix in fixes:
            data_req.fixes.add(fix)

    num_data_reqs = data_reqs.count()
    for fix in fixes:
        logger.debug('FileFix {} added to {} data requests.'.
                     format(fix.name, num_data_reqs))


    ##########
    # r2i1p1f1
    ##########
    data_reqs = DataRequest.objects.filter(
        institution_id__name='MPI-M',
        experiment_id__name__startswith='dcppc-amv',
        variant_label='r2i1p1f1'
    )

    fixes = [
        FileFix.objects.get(name='ChildBranchTime40175Add'),
        FileFix.objects.get(name='ParentBranchTime40175Add'),
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
