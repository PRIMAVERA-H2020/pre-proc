#!/usr/bin/env python2.7
"""
run_pre_proc.py

Run PRIMAVERA pre-processing as part of the CEDA CREPP workflow.
"""
import argparse
import logging.config
import os
import shutil
import sys
import tempfile

from pre_proc import EsgfSubmission
from pre_proc.common import ilist_files

__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)

PROCESSING_DIRECTORY = '/group_workspaces/jasmin2/primavera3/cache/crepp'


def create_temp_dir():
    """
    Create a temporary directory to perform the processing in.

    :returns: The path to directory created
    :rtype: str
    """
    return tempfile.mkdtemp(prefix='crepp', dir=PROCESSING_DIRECTORY)


def remove_temp_dir(temp_dir):
    """
    Delete the temporary directory created

    :param str temp_dir: The full path of the temporary directory.
    """
    if not os.listdir(temp_dir):
        os.rmdir(temp_dir)
    else:
        logger.warning('Unable to delete temporary directory as it is not '
                       'empty {}'.format(temp_dir))


def copy_file_to_temp_dir(filepath, temp_dir):
    """
    Copy the specified file into the temporary directory that's being used.

    :param str filepath: The full path of the file to copy.
    :param str temp_dir: The temporary directory to copy to.
    :returns: The new path to the file.
    :rtype: str

    """
    shutil.copy(filepath, temp_dir)

    return os.path.join(temp_dir, os.path.basename(filepath))


def move_file_to_output_dir(filepath, output_dir):
    """
    Move the file from its current location to the output directory.

    :param str filepath: The file's current full path.
    :param str output_dir: The path to the output directory.
    """
    shutil.move(filepath, output_dir)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Pre-process PRIMAVERA data.')
    parser.add_argument('input_directory', help='the directory to read files '
                                                'from', type=str)
    parser.add_argument('output_directory', help='the directory to write '
                                                 'files to', type=str)
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
    logger.debug('Database directory is {}'.
                 format(os.environ['DATABASE_DIR']))

    temp_dir = create_temp_dir()
    logger.debug('Temporary directory is {}'.format(temp_dir))

    for filepath in ilist_files(args.input_directory):
        logger.debug('Processing {}'.format(filepath))
        working_file = copy_file_to_temp_dir(filepath, temp_dir)
        esgf_submission = EsgfSubmission.from_file(working_file)
        esgf_submission.determine_fixes()
        esgf_submission.run_fixes()
        move_file_to_output_dir(working_file, args.output_directory)

    remove_temp_dir(temp_dir)

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
