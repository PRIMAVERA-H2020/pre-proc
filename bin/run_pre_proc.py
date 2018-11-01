#!/usr/bin/env python
"""
run_pre_proc.py

Run PRIMAVERA pre-processing as part of the CEDA CREPP workflow. A directory
is specified and all files in this directory are fixed. It is likely that the
same fixes will be applied to all of the files, however, the fixes to apply
are calculated again for each file.
"""
import argparse
import logging.config
import os
import sys

from pre_proc import EsgfSubmission
from pre_proc.common import list_files
from pre_proc.exceptions import PreProcError

__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Pre-process PRIMAVERA data.')
    parser.add_argument('directory', help='the directory where the files to '
                                          'fix are stored', type=str)
    parser.add_argument('-l', '--log-level', help='set logging level to one '
                                                  'of debug, info, warn (the '
                                                  'default), or error')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    return args


def main(args):
    """
    Main entry point
    """
    logger.debug('Database directory is {}'.
                 format(os.environ['DATABASE_DIR']))

    for filepath in sorted(list_files(args.directory)):
        logger.debug('Processing {}'.format(filepath))
        try:
            esgf_submission = EsgfSubmission.from_file(filepath)
            esgf_submission.determine_fixes()
            esgf_submission.run_fixes()
            esgf_submission.update_history()
        except RuntimeError:
            logger.error('Processing file {} failed'.format(filepath))
            sys.exit(1)
        except PreProcError as exc:
            logger.warning(exc)
            logger.error('Processing file {} failed'.format(filepath))
            sys.exit(1)


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
