@echo off
setlocal

set REPO_DIR=%~dp0
if "%REPO_DIR:~-1%"=="\" set REPO_DIR=%REPO_DIR:~0,-1%
set UNINSTALLER=%REPO_DIR%\installscripts\uninstall.py

where py >nul 2>nul
if not errorlevel 1 (
  py -3 "%UNINSTALLER%" %*
  exit /b %errorlevel%
)

where python >nul 2>nul
if not errorlevel 1 (
  python "%UNINSTALLER%" %*
  exit /b %errorlevel%
)

echo Python is required to run the uninstaller.
echo Install Python and run this script again.
exit /b 1
