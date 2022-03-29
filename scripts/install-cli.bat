@echo off
SET ROOT_DIR=%~dp0..


setlocal
cd /D "%ROOT_DIR%"


REM install for development
pip install --requirement cli-requirements.txt.lock
