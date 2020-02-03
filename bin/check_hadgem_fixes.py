#!/usr/bin/env python
"""
check_hadgem_fixes.py

Check through a series of test files and check that the grids and masks match
some reference files in the CEDA archive.
"""
import argparse
import logging.config
import os
import sys
import warnings

import iris
import numpy as np

from pre_proc.common import list_files

__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)

# Ignore warnings displayed when loading data
warnings.filterwarnings("ignore")


def get_reference_file(test_file, ref_base):
    """
    From `ref_base` find the path to a file that's equivalent to `test_file`.

    :param str test_file: the file being tested
    :param str ref_base: the path to the reference files in DRS format at the
        level to the variant_label. The table and then variable names can be
        appeneded to these
    :returns: the path to a suitable reference file for the specified test file
    :rtype: str
    """
    filename = os.path.basename(test_file)
    filename_cmpts = filename.split('_')
    var_name = filename_cmpts[0]
    table_name = filename_cmpts[1]
    ref_files = list_files(os.path.join(ref_base, table_name, var_name))
    if not ref_files:
        msg = f'No reference files found for {test_file} in {ref_base}'
        logger.error(msg)
        raise ValueError(msg)
    ref_files.sort()
    return ref_files[0]


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Check grids and masks')
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
    # ref_file = (
    #     '/badc/cmip6/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/historical/r1i1p1f3/'
    #     'Omon/tos/gn/v20190624/'
    #     'tos_Omon_HadGEM3-GC31-LL_historical_r1i1p1f3_gn_185001-194912.nc'
    # )
    ref_base = (
        '/badc/cmip6/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/historical/r1i1p1f3/'
    )

    test_files = [
        '/gws/nopw/j04/primavera3/cache/jseddon/test_stream1/CMIP6/HighResMIP/'
        'MOHC/HadGEM3-GC31-LL/hist-1950/r1i2p1f1/Omon/tos/gn/v20190418/'
        'tos_Omon_HadGEM3-GC31-LL_hist-1950_r1i2p1f1_gn_195001-195012.nc',
    ]

    error_encoutered = False
    for test_file in test_files:
        try:
            ref_file = get_reference_file(test_file, ref_base)
            logger.debug(ref_file)
        except ValueError:
            continue

        tube = iris.load_cube(test_file)
        rube = iris.load_cube(ref_file)

        # Test grid
        for coord_name in ['latitude', 'longitude']:
            if not np.allclose(rube.coord(coord_name).points,
                               tube.coord(coord_name).points):
                logger.error(f'Grid {coord_name} does not match the reference '
                             f'for file {test_file}')
                error_encoutered = True
        # Test mask
        if tube.coords()[0].name() == 'time':
            tube_slice = tube[0, ...]
        else:
            tube_slice = tube
        if rube.coords()[0].name() == 'time':
            rube_slice = tube[0, ...]
        else:
            rube_slice = tube
        if not np.allclose(rube_slice.data.mask, tube_slice.data.mask):
            logger.error(f'Mask does not match the reference for file '
                         f'{test_file}')
            error_encoutered = True

    if error_encoutered:
        sys.exit(1)
    else:
        sys.exit(0)


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
