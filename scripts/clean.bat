@echo off
SET ROOT_DIR=%~dp0..


setlocal
cd /D "%ROOT_DIR%"


REM clean
rmdir /S /Q build dist
