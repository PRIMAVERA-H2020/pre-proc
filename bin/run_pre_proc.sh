#!/bin/bash -l
# run_pre_proc.sh
# A wrapper around run_pre_proc.py to set the appropriate environment
# variables.
INSTALL_DIR=/home/users/jseddon/primavera/pre-proc
CONDA_DIR=/home/users/jseddon/software/miniconda3/bin
CONDA_ENV_DIR=/home/users/jseddon/software/miniconda3/envs/py3-6_iris2-3/bin

# Force NumPy not to parallelise
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

export PATH=$CONDA_DIR:$PATH
. activate py3-6_iris2-3
export DJANGO_SETTINGS_MODULE=pre_proc_site.settings
export PYTHONPATH=$INSTALL_DIR:$INSTALL_DIR/HighResMIP-fix:$INSTALL_DIR/cmor-fixer

export DATABASE_DIR=`mktemp -d /tmp/prima-crepp.XXXXXXX`
cp $INSTALL_DIR/db/pre-proc_db.sqlite3 $DATABASE_DIR

$CONDA_ENV_DIR/python $INSTALL_DIR/bin/run_pre_proc.py -l debug "$@"
RETURN_CODE=$?

rm $DATABASE_DIR/pre-proc_db.sqlite3
rmdir $DATABASE_DIR

exit $RETURN_CODE
