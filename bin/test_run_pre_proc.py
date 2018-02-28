#!/usr/bin/env python2.7
"""
run_pre_proc.py

Run PRIMAVERA pre-processing as part of the CEDA CREPP workflow.

This is currently a test and a single processing item has been hard-coded.
"""
import argparse
import logging.config
import sys

from pre_proc import ParentBranchTimeDoubleFix, ChildBranchTimeDoubleFix


__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

TMPDIR = '/var/tmp'

logger = logging.getLogger(__name__)



def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Pre-process PRIMAVERA data.')
    parser.add_argument('-l', '--log-level', help='set logging level to one '
        'of debug, info, warn (the default), or error')
    parser.add_argument('--version', action='version',
        version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    return args


def main(args):
    """
    Main entry point
    """
    fixer = ParentBranchTimeDoubleFix(
        ['tas_Amon_HadGEM3-GC31-LL_control-1950_r1i1p1f1_gn_195001-195012.nc'],
        '/scratch/jseddon/sandbox'
    )
    fixer.apply_fix()

    fixer = ChildBranchTimeDoubleFix(
        ['tas_Amon_HadGEM3-GC31-LL_control-1950_r1i1p1f1_gn_195001-195012.nc'],
        '/scratch/jseddon/sandbox/output'
    )
    fixer.apply_fix()


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
    main(cmd_args)
