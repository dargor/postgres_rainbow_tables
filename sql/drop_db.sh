#!/bin/sh
set -eu

psql --no-psqlrc -U postgres -c 'drop database rainbows'

echo DONE
