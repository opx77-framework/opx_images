@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python tools\upload-images.py %*
) else (
  py -3 tools\upload-images.py %*
)
if errorlevel 1 (
  echo Upload failed. Check that Python 3 is installed.
  pause
  exit /b 1
)
pause
