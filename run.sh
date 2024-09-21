#!/bin/bash

set -e

MODE="prod"
HOST="0.0.0.0"
PORT="8000"

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --dev)
            MODE="dev"
            ;;
        --host)
            HOST="$2"
            shift
            ;;
        --port)
            PORT="$2"
            shift
            ;;
        *)
            # Unknown option
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
    shift
done

python manage.py migrate 2>&1 | tee logs/migrate.log

if [ "$MODE" == "dev" ]; then
    python manage.py runserver "$HOST:$PORT" --settings="settings_dev.py" 2>&1 | tee logs/runserver.log
else
    python manage.py runserver "$HOST:$PORT" 2>&1 | tee logs/runserver.log
fi
