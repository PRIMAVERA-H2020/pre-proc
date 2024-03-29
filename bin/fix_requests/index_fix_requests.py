#!/usr/bin/env python
"""
index_fix_requests.py

This file builds an HTML summary of the Python files in this directory.

The file naming convention is assumed to be:

1*** AWI
2*** CMCC
3*** CNRM-CERFACS
4*** EC-Earth-Consortium
5*** ECMWF
6*** MOHC
7*** NERC
8*** MPI

*0** All experiments
*1** All AMIP
*2** highresSST-present
*3** highresSST-future
*4** All coupled
*5** spinup-1950
*6** control-1950
*7** hist-1950
*8** highres-future
*9** wp5

The docstring at the top of every file is assumed to be in the form (index of
docstring line on the left):
0  filename.py                                            [ignored]
1                                                         [blank line]
2 MOHC.HadGEM3-GC31-*.highresSST-present.r1i1p1f1.Amon.*  [Affected variables]
3                                                         [blank line]
4 Description                                             [description]
5 continued.....
"""
import argparse
import glob
import importlib
import logging.config
import os
import re
import sys

__version__ = '0.1.0b1'

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = '%(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


HTML_FILE = 'fix_requests.html'


def _ouput_headers(fh):
    txt = """<html>
<head>
<style>
.Body { background-color: #eeeeee;
 font-family: Verdana, "Arial", Helvetica, sans-serif; margin: 0px}
#titleBar {     background-color: #dddddd;
                width: 100%;
                top: 3px; 
                border-top: solid #aaaaaa 1px;  
                border-bottom: solid #aaaaaa 1px; 
                padding:6px;
                position: relative}
                
#blurb {        padding-left: 20px;
                padding-right: 20px;
                padding-top: 30px;
                padding-bottom:15px }
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
}
</style>
<title>fix_requests</title>
</head>
<body class="Body">
<div id="titleBar"><b>fix_requests</b></div>
<div id="blurb">
<table>\n
"""
    fh.write(txt)


def _ouput_footers(fh):
    txt = """
</table>
</div>
</body>
</html>
"""
    fh.write(txt)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Index the docstrings of the '
                                                 'fix_request_*.py scripts')
    parser.add_argument('-l', '--log-level', help='set logging level to one of '
                                                  'debug, info, warn (the '
                                                  'default), or error')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    return args


def main():
    """
    Main entry point
    """
    update_dir = os.path.dirname(__file__)
    update_files = glob.glob(os.path.join(update_dir, 'fix_request_*.py'))
    update_files.sort()

    with open(os.path.join(update_dir, HTML_FILE), 'w') as fh:
        _ouput_headers(fh)
        for update_file in update_files:
            import_string = os.path.basename(update_file.rstrip('.py'))
            doc_string = importlib.import_module(import_string).__doc__
            file_name = os.path.basename(update_file)
            file_index = re.findall(r'\d+', file_name)[0]
            affected_drs = doc_string.split('\n')[3]
            description = '\n'.join(doc_string.split('\n')[5:])
            fh.write('<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n'.
                     format(file_index, affected_drs, description))
        _ouput_footers(fh)


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
