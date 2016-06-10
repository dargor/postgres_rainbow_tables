#!/bin/sh
set -eu

psql --no-psqlrc -U postgres -f db.sql -v ON_ERROR_STOP=1

echo DONE
