@echo off
SET ROOT_DIR=%~dp0..


setlocal
cd /D "%ROOT_DIR%"


REM tests pass?
scripts\install-dev.bat
if %errorlevel% neq 0 exit /b %errorlevel%

scripts\test.bat
if %errorlevel% neq 0 exit /b %errorlevel%

REM release
scripts\clean.bat
scripts\build.bat
scripts\release.bat
