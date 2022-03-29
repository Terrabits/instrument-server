@echo off
SET ROOT_DIR=%~dp0..


setlocal
cd /D "%ROOT_DIR%"


REM build cli
pyinstaller cli.spec
