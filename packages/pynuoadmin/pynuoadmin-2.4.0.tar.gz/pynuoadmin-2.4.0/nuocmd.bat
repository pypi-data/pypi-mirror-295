@echo off
REM -- Invoke the NuoDB command-line tool
REM (C) Copyright 2017-2023 Dassault Systemes SE.  All Rights Reserved.

setlocal

if not "%NUODB_HOME%" == "" goto findpy

pushd %~dp0..
set "NUODB_HOME=%CD%"
popd

:findpy
if "%NUOPYTHON%" == "" goto trypy3
set "pycmd=%NUOPYTHON%"
goto run

:trypy3
where /q python3
if ERRORLEVEL 1 goto trypy
set "pycmd=python3"
goto run

:trypy
where /q python
if ERRORLEVEL 1 (
    echo No Python interpreter found: please install and update PATH
    exit /b 1
)
set "pycmd=python"

:run
set "PYTHONPATH=%NUODB_HOME%\etc\python\site-packages;%PYTHONPATH%"
"%pycmd%" -u -m pynuoadmin.nuocmd %*
