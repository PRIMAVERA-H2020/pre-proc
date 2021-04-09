
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3904596.svg)](https://doi.org/10.5281/zenodo.3904596)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# pre-proc
Copyright (c) 2021, PRIMAVERA
Please see LICENSE for further details

PRIMAVERA pre_proc system for fixing metadata and data issues in netCDF files (particularly CMIP6 data). Pre_proc works by:

1. fixes (a Python class) are written to fix small individual errors in a file's metadata or data. Abstract classes have been developed, which allow new fixes to be rapidly written, often only taking a line or two of new code. The fixes can make use of tools such as `ncatted` to run the fixes, or pure Python fixes could also be written. Unit tests have been written for all of the existing tests to provide assurance of their quality.
2. a list of datasets (data requests) that exist is added to pre_proc's database
3. rules are written that determine which fixes are added to groups of datasets
4. the `run_pre_proc.sh` script is run to fix the data. The script takes a single argument, the path to a directory of netCDF files. The script identifies which (if any) fixes need to be applied to each file and applies the fixes in alphabetical order of class name.

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

A Rose suite has been developed to provide optional control and monitoring of pre_proc. `u-av973` is the suite's id.

To add new data requests to the Rose suite:

1. In the DMT code: `./scripts/make_esgf_json.py -l debug <filename.json>` to get the data requests that files have been received for.
1. `./bin/make_db_from_json.py -l debug <filename.json>` to add any new data requests to the pre-proc database.
1. In the DMT code edit and then run: `./scripts/make_rose_task_names.py -l debug <~/temp/rose_task_names.json>`
1. Make the Rose suite aware of these new tasks: `rose suite-run --reload --no-gcontrol`
1. In the Rose suite (but under Python 3): `bin/add_new_tasks.py -l debug <rose_task_names_new.json>`  

pre-proc uses the Django framework for database access. The database is an sqlite database that allows fixes to be mapped to data requests. To run the tests: `python manage.py test`.
