@echo off

:: Fetch param1
set "param1=%~1"

:: Execute python with argument
py -3 ./wdc/wdc.py %param1%
