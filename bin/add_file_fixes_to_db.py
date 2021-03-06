#!/usr/bin/env python
"""
add_file_fixes_to_db.py

Load the available file fixes into the database.
"""
import argparse
import logging.config
import sys

import django
django.setup()

from django.template.defaultfilters import pluralize

import pre_proc
from pre_proc.common import get_concrete_subclasses
from pre_proc_app.models import FileFix


__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Pre-process PRIMAVERA data.')
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
    file_fixes = [
        klass.__name__
        for klass in get_concrete_subclasses(pre_proc.file_fix.FileFix)
    ]

    num_created = 0
    added_names = []
    for file_fix_name in file_fixes:
        inst, created = FileFix.objects.get_or_create(name=file_fix_name)
        if created:
            num_created += 1
            added_names.append(file_fix_name)

    logger.debug('Added {} new FileFix object{}.'.format(num_created,
                                                         pluralize(
                                                             num_created)))
    if num_created:
        logger.debug('Added: {}'.format(', '.join(added_names)))


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
