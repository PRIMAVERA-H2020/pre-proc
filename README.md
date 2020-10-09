[![DOI](https://zenodo.org/badge/122643471.svg)](https://zenodo.org/badge/latestdoi/122643471) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# pre-proc
Copyright (c) 2020, PRIMAVERA
Please see LICENSE.md for further details

PRIMAVERA Pre-Proc script for submission to ESGF

To set up the system:

1. `mkdir db`
1. `touch db/pre-proc_db.sqlite3`
1. `export DJANGO_SETTINGS_MODULE=pre_proc_site.settings`
1. `export PYTHONPATH=.`
1. `export DATABASE_DIR=/home/users/jseddon/primavera/pre-proc/db`
1. `python manage.py migrate`
1. (If using the DMT) in the DMT code: `./scripts/make_esgf_json.py -l debug <filename.json>` to get the data requests that files have been received for.
1. `./bin/make_db_from_json.py -l debug <filename.json>` to add the data requests. `example_data_requests.json` shows an example of this file.
1. `./bin/add_file_fixes_to_db.py -l debug` to add the file fixes to the database.
1. Run all of the fix_request scripts, e.g. `./bin/fix_requests/fix_request_0001.py -l debug` to set up the file fixes required for each data request.

If additional data requests are added then all of the fix_request
scripts will need to be run again.

It should now be possible to run the main processing script:

`./bin/run_pre_proc.sh <data_dir>`

To add new data requests to the Rose suite:

1. In the DMT code: `./scripts/make_esgf_json.py -l debug <filename.json>` to get the data requests that files have been received for.
1. `./bin/make_db_from_json.py -l debug <filename.json>` to add any new data requests to the pre-proc database.
1. In the DMT code edit and then run: `./scripts/make_rose_task_names.py -l debug <~/temp/rose_task_names.json>`
1. Make the Rose suite aware of these new tasks: `rose suite-run --reload --no-gcontrol`
1. In the Rose suite (but under Python 3): `bin/add_new_tasks.py -l debug <rose_task_names_new.json>`  
