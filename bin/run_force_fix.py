#!/usr/bin/env python
"""
run_force_fix.py

Run PRIMAVERA pre-processing as part of the CEDA CREPP workflow. A directory
is specified and all files in this directory are fixed with the specified
FileFix.
"""
import argparse
import logging.config
import os
import sys
import traceback
import warnings

import dask

import pre_proc
from pre_proc import EsgfSubmission
from pre_proc.common import list_files

__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)

# Ignore warnings displayed when loading data
warnings.filterwarnings("ignore")


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Pre-process PRIMAVERA data.')
    parser.add_argument('directory', help='the directory where the files to '
                                          'fix are stored', type=str)
    parser.add_argument('fix_name', help='the name of the FileFix class '
                                         'to apply', type=str)
    parser.add_argument('-f', '--file', help='Process single file rather than '
                                             'directory',
                        action='store_true')
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
    # Assume that this will be run with one CPU allocated
    dask.config.set(scheduler='synchronous')

    logger.debug('Database directory is {}'.
                 format(os.environ['DATABASE_DIR']))

    files_failed = []

    if args.file:
        files_to_process = [args.directory]
    else:
        files_to_process = sorted(list_files(args.directory))

    for filepath in files_to_process:
        logger.debug('Processing {}'.format(filepath))
        try:
            esgf_submission = EsgfSubmission.from_file(filepath)
            esgf_submission.fixes = [getattr(pre_proc.file_fix, args.fix_name)
                                     (os.path.basename(filepath),
                                      os.path.dirname(filepath))]
            esgf_submission.run_fixes()
            esgf_submission.update_history()
        except:
            files_failed.append(filepath)
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb_list = traceback.format_exception(exc_type, exc_value, exc_tb)
            tb_string = '\n'.join(tb_list)
            logger.error('Processing file {} failed\n{}'.
                         format(filepath, tb_string))

    if files_failed:
        logger.error('{} files failed:\n{}'.format(len(files_failed),
                                                   '\n'.join(files_failed)))
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
