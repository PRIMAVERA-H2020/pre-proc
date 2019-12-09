#!/bin/bash -l
# run_single_file.sh
# A wrapper around run_single_file.py to set the appropriate environment
# variables.
INSTALL_DIR=/home/users/jseddon/primavera/pre-proc
CONDA_DIR=/home/users/jseddon/software/miniconda3/bin
CONDA_ENV_DIR=/home/users/jseddon/software/miniconda3/envs/py3-6/bin

export PATH=$CONDA_DIR:$PATH
. activate py3-6
export DJANGO_SETTINGS_MODULE=pre_proc_site.settings
export PYTHONPATH=$INSTALL_DIR:$INSTALL_DIR/HighResMIP-fix:$INSTALL_DIR/cmor-fixer

export DATABASE_DIR=`mktemp -d /tmp/prima-crepp.XXXXXXX`
cp $INSTALL_DIR/db/pre-proc_db.sqlite3 $DATABASE_DIR

$CONDA_ENV_DIR/python $INSTALL_DIR/bin/run_single_file.py -l debug "$@"
RETURN_CODE=$?

rm $DATABASE_DIR/pre-proc_db.sqlite3
rmdir $DATABASE_DIR

exit $RETURN_CODE
