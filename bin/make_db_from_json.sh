#!/bin/bash -l
# make_db_from_json.sh
# A wrapper around make_db_from_json.py to set the appropriate environment
# variables.
INSTALL_DIR=/home/users/jseddon/primavera/pre-proc
DATABASE_DIR=$INSTALL_DIR/db
CONDA_DIR=/home/users/jseddon/software/miniconda3/bin
CONDA_ENV_DIR=/home/users/jseddon/software/miniconda3/envs/py3-6/bin

export PATH=$CONDA_DIR:$PATH
. activate py3-6
export DJANGO_SETTINGS_MODULE=pre_proc_site.settings
export PYTHONPATH=$INSTALL_DIR

$CONDA_ENV_DIR/python $INSTALL_DIR/bin/make_db_from_json.py "$@"
