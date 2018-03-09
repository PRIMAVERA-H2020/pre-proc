# pre-proc
PRIMAVERA Pre-Proc script for submission to ESGF

To set up the system:

1. `mkdir db`
1. `touch db/pre-proc_db.sqlite3`
1. `export DJANGO_SETTINGS_MODULE=pre_proc_site.settings`
1. `export PYTHONPATH=.`
1. `export DATABASE_DIR=/home/users/jseddon/primavera/pre-proc/db`
1. `python manage.py migrate`
1. In the DMT code: `./scripts/make_esgf_json.py -l debug <filename.json>` to get the data requests that files have been received for.
1. `./bin/make_db_from_json.py -l debug <filename.json>` to add the data requests.
1. `./bin/add_file_fixes_to_db.py -l debug` to add the file fixes to the database.
1. Run all of the fix_request scripts, e.g. `./bin/fix_requests/fix_request_0001.py -l debug` to set-up the file fixes required for each data request.

It should now be possible to run the main processing script:

`./bin/run_pre_proc.sh <input_dir> <output_dir>`
