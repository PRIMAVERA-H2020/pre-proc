#!/bin/bash -l
# run_pre_proc.sh
# A wrapper around run_pre_proc.py to set the appropriate environment
# variables.
INSTALL_DIR=/home/users/jseddon/primavera/pre-proc

source $INSTALL_DIR/../venvs/django/bin/activate
export DJANGO_SETTINGS_MODULE=pre_proc_site.settings
export PYTHONPATH=.


export DATABASE_DIR=`mktemp -d /tmp/prima-crepp.XXXXXXX`
cp $INSTALL_DIR/db/pre-proc_db.sqlite3 $DATABASE_DIR

python2.7 $INSTALL_DIR/bin/run_pre_proc.py -l debug "$@"

rm $DATABASE_DIR/pre-proc_db.sqlite3
rmdir $DATABASE_DIR
