@echo off
setlocal enabledelayedexpansion

REM
set MODE=prod
set HOST=0.0.0.0
set PORT=8000

REM
:parse_args
if "%1" == "--dev" (
    set MODE=dev
) else if "%1" == "--host" (
    set HOST=%2
    shift
) else if "%1" == "--port" (
    set PORT=%2
    shift
) else if "%1" == "" (
    goto run_commands
) else (
    echo Unknown option: %1
    exit /b 1
)
shift
goto parse_args

:run_commands
REM
python manage.py migrate 2>&1 | tee logs\migrate.log

if "%MODE%" == "dev" (
    python manage.py runserver %HOST%:%PORT% --settings="settings_dev.py" 2>&1 | tee logs\runserver.log
) else (
    python manage.py runserver %HOST%:%PORT% 2>&1 | tee logs\runserver.log
)
