#!/bin/sh
set -eu

python backend/manage.py check
if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    python backend/manage.py migrate --noinput
fi

# Demo accounts require an explicit, separate seed_db command.
exec "$@"
