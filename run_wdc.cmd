@echo off

:: Fetch param1
set "param1=%~1"

:: Change directories to wdc. This helps with relative path
cd wdc

:: Execute python with argument
py -3 wdc.py %param1%

:: Go back where ya came from
cd ..
