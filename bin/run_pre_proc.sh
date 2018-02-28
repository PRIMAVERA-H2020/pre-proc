#!/bin/bash -l
# run_pre_proc.sh
# A wrapper around run_pre_proc.py to set the appropriate environment
# variables.
INSTALL_DIR=/home/h04/jseddon/primavera/pre-proc

source /home/h04/jseddon/primavera/venvs/django/bin/activate
export DJANGO_SETTINGS_MODULE=pre_proc_site.settings
export PYTHONPATH=.

python2.7 $INSTALL_DIR/bin/run_pre_proc.py -l debug "$@"
