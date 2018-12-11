#!/bin/bash -l
# run_pre_proc.sh
# A wrapper around run_pre_proc.py to set the appropriate environment
# variables.
INSTALL_DIR=/home/users/jseddon/primavera/pre-proc
CONDA_DIR=/group_workspaces/jasmin2/primavera1/tools/miniconda2/bin
CONDA_ENV_DIR=/group_workspaces/jasmin2/primavera1/tools/miniconda2/envs/py3-6/bin

export PATH=$CONDA_DIR:$PATH
. activate py3-6
export DJANGO_SETTINGS_MODULE=pre_proc_site.settings
export PYTHONPATH=$INSTALL_DIR

export DATABASE_DIR=`mktemp -d /tmp/prima-crepp.XXXXXXX`
cp $INSTALL_DIR/db/pre-proc_db.sqlite3 $DATABASE_DIR

$CONDA_ENV_DIR/python $INSTALL_DIR/bin/run_pre_proc.py -l debug "$@"
RETURN_CODE=$?

rm $DATABASE_DIR/pre-proc_db.sqlite3
rmdir $DATABASE_DIR

exit $RETURN_CODE
